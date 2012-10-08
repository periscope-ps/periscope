import sys
import time
from unis_client import UNISInstance
from collector import Collector
from multiprocessing import  Process, Pipe
from utils import *
import settings
from pprint import pprint

logger = settings.get_logger('sched_obj')

class SchedObj:
    def __init__(self, probe_name, settings_name="settings"):
        self.probe_settings=try__import__(probe_name+"_settings")
        self.settings=try__import__(settings_name)
        self.probe_module=try__import__(probe_name)
        self.mids = {}
        self.collector = None
        self.unis = None
        self.probe = None
        self.start_time = None
        self.end_time = None
        self.c_iteration = 0 # which collection are we on
        self.r_iteration = 1

    def run(self, conn):
        self.read_settings()
        if self.probe==None:
            return
        # main collection loop
        self.start_time = time.time()
        cur_time = self.start_time
        while cur_time < self.end_time:
            # check for communication - reload if sched says so
            if conn.poll():
                if conn.recv()=='reload':
                    logger.info('reload')
                    ### Flush collector first?
                    self._sreload()
            cur_time = time.time()
            # time to collect?
            if cur_time >= (self.c_iteration*self.ci+self.start_time):
                self.collect()
            # time to report?
            if cur_time >= (self.r_iteration*self.ri+self.start_time):
                self.report()
            # calculate amount to sleep
            if self.sleep_factor>0:
                self.sleep()
            cur_time = time.time()
                
    def collect(self):
        logger.info('collect')
        self.c_iteration += 1
        ts = time.time()
        data = self.probe.get_data()
        self._insert_data(data, ts)

    def report(self):
        logger.info('report')
        self.r_iteration += 1
        self.collector.report()

    def sleep(self):
        next_rtime=self.r_iteration*self.ri+self.start_time
        next_ctime=self.c_iteration*self.ci+self.start_time
        cur_time=time.time()
        if next_rtime<next_ctime:
            sleep_time=next_rtime-cur_time
        else:
            sleep_time=next_ctime-cur_time
        sleep_time=self.sleep_factor*sleep_time
        if sleep_time>0:
            time.sleep(sleep_time)

    def _insert_data(self, data, ts):
        # give data to collector, taking into account that
        # data might be {"metric":value,...} or
        # {"subject":{"metric":value, ...}, ...}
        for thing in data:
            if isinstance(data[thing], dict):
                subject=thing
                for metric,value in data[subject].iteritems():
                    mid=self._get_mid(subject, metric)
                    self.collector.insert(mid, ts, value)
            else:
                metric=thing
                mid=self._get_mid(self.settings.SUBJECT, metric)
                value=data[metric]
                self.collector.insert(mid, ts, value)

    def _get_mid(self, subject, metric):
        return self.mids[subject][metric]

    def _register_metadata(self):
        data=self.probe.get_data()
        for item in data:
            if isinstance(data[item], dict):
                for metric in data[item]:
                    self._post_metadata(item, metric)
            else:
                self._post_metadata(self.settings.SUBJECT, item)
        ts = time.time()
        self._insert_data(data, ts)
        self.collector.create_collections()

    def _post_metadata(self, subject, metric):
        e_t=self.event_types[metric]
        params = {"datumSchema": self.schemas["datum"],
                  "collectionInterval": self.ci
                  }
        post = dict({"$schema":self.schemas['metadata'],
                     "subject": dict({"href":subject,
                                      "rel":"full"}),
                     "eventType":e_t,
                     "parameters":params})
        resp = self.unis.post_metadata(post)
        if isinstance(resp, dict):
            print resp
            self.collector.update_metadatas(resp)
            self._update_local_mids(subject, metric, resp["id"])
        else:
            logger.error('post_metadata.failed')
            sys.exit(1)
            


    def _update_local_mids(self, subject, metric, mid):
        if not subject in self.mids:
            self.mids.update({subject:{}})
        self.mids[subject][metric]=mid

    def _get_setting(self, setting_name, def_val):
        try:
            ret=self.probe_settings.__getattribute__(setting_name)
        except AttributeError:
            try:
                ret=self.settings.__getattribute__(setting_name)
            except AttributeError:
                ret=def_val
        return ret
    
    def reload_settings(self):
        self.probe_settings=reload(self.probe_settings)
        self.settings=reload(self.settings)
        self.read_settings()
        
    def read_settings(self):
        ### should refresh unis and collector only if urls or whatever change
        # sets up class variables from settings files, with some validation
        self.ci=self._get_setting("COLLECTION_INTERVAL", 30)
        self.ri=self._get_setting("REPORTING_INTERVAL", 300)
        self.ctime=self._get_setting("COLLECTION_TIME", 0)
        self.sleep_factor=self._get_setting("SLEEP_FACTOR", 1)
        self.coll_size=self._get_setting("COLLECTION_SIZE", 10000)
        self.coll_ttl=self._get_setting("COLLECTION_TTL", 10000)
        self.event_types=self._get_setting(
            "EVENT_TYPES", FakeDict("EVENT_TYPES"))
        self.schemas=self._get_setting("SCHEMAS", FakeDict("SCHEMAS"))
        self.md_cache=self._get_setting("METADATA_CACHE", "/tmp/blippmd")
        self.outfile=self._get_setting("OUTPUT_FILE", None)
        self.unis_url=self._get_setting("UNIS_URL", None)
        self.ms_url=self._get_setting("MS_URL", None)
        self.kwargs=self._get_setting("KWARGS", {})
        self.check_interval=self._get_setting("CHECK_INTERVAL", 1)

        if self.sleep_factor<0 or self.sleep_factor>1:
            self.sleep_factor=1

        if self.ri<self.ci:
            self.ri=self.ci

        if self.probe_module is not None:
            self.probe=self.probe_module.Probe(kwargs=self.kwargs)
        else:
            self.probe=None

        self.unis = UNISInstance(self.unis_url)
        self.collector = Collector(self.ms_url, self.coll_size,
                                   self.coll_ttl, self.outfile)
        self._register_metadata()
        # set up collection time
        self.start_time=time.time()
        self.end_time=self.start_time+self.ctime
        if self.end_time==self.start_time:
            self.end_time=sys.maxint

        self.last_rtime = 0 # last time measurements were reported
        self.last_ctime = 0 # last time measurements were collected




class FakeDict:
    '''Returns a default string when queried with brackets'''
    def __init__(self, desc):
        self.def_schema="http://set."+str(desc)+".dict.in.settings.py"
    def __getitem__(self, query):
        return self.def_schema + ".with.key." + str(query)
