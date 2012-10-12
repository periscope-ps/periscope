import time
import json
import requests
import sys
import uuid
import os
from stat import ST_MTIME
from multiprocessing import Process, Pipe

from ms_client import MSInstance
from unis_client import UNISInstance
from collector import Collector
from sched_obj import SchedObj, FakeDict

import settings

logger = settings.get_logger('sched')
SETTINGS_FILE = os.path.dirname(__file__) + "/settings.py"
if settings.DEBUG:
    for item in dir(settings):
        if ord(item[0])>=65 and ord(item[0])<=90:
            logger.debug('settings',
                         item=item,
                         value=str(settings.__getattribute__(item))) #@UndefinedVariable


# loop every check interval:
#    check settings file and reload
#    check probe_settings files and add to probes_reload if changed
#    loop probes:
#        does it have a process?
#            no: create and start it
#            yes: is it not alive?
#                join it check exit code
#                based on exit code restart it or not
#    loop procs:
#        is it not in probes?
#            join/send stop/kill it.
#        is it in probes_reload?
#            send "reload"



class Scheduler():
    def __init__(self):
        self.probes = settings.PROBES
        self.procs = {}
        self.conns = {}
        self.mtimes = {}
        self.sched_objs = {}
        self.settings_mtime = self._get_mtime(SETTINGS_FILE)
        self.probes_reload = []

    def check_settings(self):
        latest = self._get_mtime(SETTINGS_FILE)
        if self.settings_mtime<latest:
            self.settings_mtime=latest
            settings = reload(settings)
            self.probes = settings.PROBES
        for name in self.probes:
            latest = self._get_mtime(os.path.dirname(__file__)+ "/" + name + "_settings.py")
            if not self.mtimes.has_key(name):
                self.mtimes[name]=latest
            if self.mtimes.get(name, sys.maxint)<latest:
                self.mtimes[name]=latest
                self.probes_reload.append(name)

    def check_probes(self):
        for probe in self.probes:
            proc = self.procs.get(probe, None)
            if proc:
                if not proc.is_alive():
                    self._handle_dead_proc(proc)
                    self._cleanup_probe(probe)
            else:
                self._setup_probe(probe)
                
    def check_procs(self):
        for name,proc in self.procs.items():
            if name not in self.probes:
                self._stop_proc(proc, name)
                self._cleanup_probe(name)
            elif name in self.probes_reload:
                self.conns[name].send("reload")
                self.probes_reload.remove(name)

    def _stop_proc(self, proc, name):
        # maybe we send it a stop through the connection
        # maybe we just terminate it
        # iunno
        logger.warn('scheduler.stop_proc', probe=name)
        proc.terminate()

    def _cleanup_probe(self, name):
        del self.procs[name]
        del self.sched_objs[name]
        del self.conns[name]
        del self.mtimes[name]
        
                
    def _setup_probe(self, name):
        if not self.sched_objs.get(name, None):
            self.sched_objs[name] = SchedObj(name)
        parent_conn, child_conn = Pipe()
        self.procs[name]=Process(target=self._run_sched_obj,
                                 args=(self.sched_objs[name], child_conn,))
        self.conns[name]=parent_conn
        logger.info('scheduler.setup_probe.start', probe=name)
        self.procs[name].start()
        
    def _handle_dead_proc(self, proc):
        if proc.exitcode < 0:
            logger.error('scheduler.handle_dead_probe',
                         exitcode=str(proc.exitcode))
        elif proc.exitcode == 0:
            logger.error('scheduler.handle_dead_probe',
                         exitcode=str(proc.exitcode))
        elif proc.exitcode>0:
            logger.error('scheduler.handle_dead_probe',
                         exitcode=str(proc.exitcode))
        else:
            logger.error('scheduler.handle_dead_probe',
                         exitcode=str(proc.exitcode))
        proc.join()
        
    def _run_sched_obj(self, sched_obj, conn):
        sched_obj.run(conn)
        
    def _get_mtime(self, fname):
        try:
            st = os.stat(fname)
        except IOError as e:
        ### LOG unable to read settings file
            logger.exc('scheduler.get_mtime', e)
            return 0
        return st[ST_MTIME]


def main():
    unis_client = UNISInstance(unis_url=settings.UNIS_URL)
    unis_client.register_service_to_unis()
    s = Scheduler()
    while 1:
        start_time=time.time()
        s.check_settings()
        s.check_probes()
        s.check_procs()
        sleep_time = (start_time+settings.CHECK_INTERVAL)-time.time()
        if sleep_time > .001:
            time.sleep(sleep_time)
        

if __name__=="__main__":
    main()

def run_probe(probe_obj, conn):
    cur_time = time.time()
    while cur_time < probe_obj.end_time:
        pass
