from ms_client import MSInstance
import json

from pprint import pprint

import settings
logger = settings.get_logger('collector')

class Collector:
    """Collects reported measurements and aggregates them for
    sending to MS at appropriate intervals.
    """
    POST_DATA_SUCCESS = 201
    def __init__(self, ms_url=None, coll_size=10000,
                 coll_ttl=10000, outfile=None, do_print=False):
        self.metadatas = []
        self.datas = {} # dict keyed on mid. value is list of
                        # {"ts":ts, "value":val}
        self.collections_created = False
        if ms_url is None:
            self.ms=None
        else:
            self.ms = MSInstance(ms_url)
        self.coll_size=coll_size
        self.coll_ttl=coll_ttl
        if outfile:
            self.outfile=open(outfile, 'w')
        else:
            self.outfile=None
        self.do_print=do_print

    def insert(self, mid, ts, val):
        item = dict({"ts": ts * 1000000,
                     "value":val})
        if not self.datas.has_key(mid):
            self.datas[mid]=[]
        self.datas[mid].append(item)

    def report(self):
        ### need to make sure collections are created before reporting
        data = self._format_datas()
        if self.ms:
            r = self.ms.post_data(data)
            if r == self.POST_DATA_SUCCESS:
                self._clear_datas()
        if self.outfile:
            try:
                self.outfile.write(json.dumps(data))
                if not self.ms: # if there is an ms, save the data for it
                    self._clear_datas()
            except Exception as e:
                logger.exc('report', e)
        if self.do_print or not (self.ms or self.outfile):
            pprint(data) 
            if not self.ms: # if there is an ms, save the data for it
                self._clear_datas()
                
        ### The following line turns off all measurement caching... if the ms goes down
        ### when blipp tries to report, that set of measurements will be lost
        self._clear_datas()

    def _clear_datas(self):
        for mid in self.datas:
            self.datas[mid]=[]
            
    def _format_datas(self):
        ret = []
        for mid in self.datas:
            item = dict({"mid":mid,
                        "data":self.datas[mid]})
            ret.append(item)
        return ret

    def set_metadatas(self, metadatas):
        '''Replace the collectors list of metadatas with those
        passed in'''
        if isinstance(metadatas, list):
            ### Need some verification here
            self.metadatas=metadatas
        elif isinstance(metadatas, dict):
            ### And here
            self.metadatas=[metadatas]
        else:
            ### LOG issue in set_metadata
            print "Collector: set_metadatas: metadata is of invalid format"

    def update_metadatas(self, metadatas):
        '''Update the collectors list of metadatas with those that are
        passed in'''
        if isinstance(metadatas, list):
            ### Need some verification here
            self.metadatas=self.metadatas+metadatas
        elif isinstance(metadatas, dict):
            ### And here
            self.metadatas.append(metadatas)
        else:
            ### LOG issue in update_metadatas
            print "Collector: update_metadatas: metadata is of invalid format"

    def create_collections(self, metadatas=None):
        '''Create collections in the MS for the metadata that the
        collector already knows about, or for the list of metadatas
        that is passed in'''
        if not self.ms:
            logger.warn('create_collections', message="No MS specified")
            return
        if metadatas is None:
            metadatas=self.metadatas
        elif isinstance(metadatas, dict):
            metadatas=[metadatas]
        elif not isinstance(metadatas, list):
            logger.error('create_collections', metadatas=str(metadatas))
            return

        self.created_collections=True
        for md in metadatas:
            r = self.ms.post_events(md["selfRef"], self.coll_size,
                                        self.coll_ttl)
            if not (r>=200 and r<300):
                self.created_collections=False
            ### uh.... handle response somehow
            
            
