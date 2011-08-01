"""
Base classes for classification
"""

from _base import Method

def distance(x, y):
    d=0
    for i in x:
        d = d + (x[i]-y[i]) * (x[i]-y[i])
    return d
    pass

class OnlineClassify(Method):
    """distance-based classifier
    """
    def __init__(self, src, sink, clusters):
        """Initialize with data source and sink.

        Args:
          src - eventQueue.
          sink - Obj supporting DataSink interface.
          clusters -  list of cluster centers.
        """
        self.jobInfo = {}
        self.stateMap = {
            'SUBMIT': self.handleSubmit,
            'EXECUTE': self.handleExecute,
            'JOB_SUCCESS': self.handleSuccess,
            'JOB_FAILURE': self.handleFailure,
            'JOB_ABORTED': self.handleAbort,
            'JOB_TERMINATED': self.noop,
            'JOB_EVICTED': self.noop,
            'SUBMIT_FAILED': self.noop,
            'JOB_DISCONNECTED': self.noop,
            'POST_SCRIPT_STARTED': self.noop,
            'POST_SCRIPT_SUCCESS': self.noop,
            'POST_SCRIPT_FAILURE': self.noop,
            'POST_SCRIPT_TERMINATED': self.noop,
            'SHADOW_EXCEPTION': self.noop,
            'IMAGE_SIZE': self.noop,
            'GLOBUS_SUBMIT': self.noop,
            'JOB_RECONNECT_FAILED': self.noop,
            'GRID_SUBMIT': self.noop,
            'JOB_HELD': self.noop,
            'JOB_RELEASED':self.noop,
            'JOB_UNSUSPENDED': self.noop,
            'SUBMIT_FAILED': self.noop,
            'JOB_RECONNECTED': self.noop,
            'PRE_SCRIPT_STARTED': self.noop,
            'PRE_SCRIPT_SUCCESS': self.noop
        }
        self.eventMap = {
            'stampede.workflow.plan' : self.handleWf,
            'stampede.wrokflow.start' : self.handleWf,
            'stampede.workflow.end' :self.handleWf
        }

        self.clusters = clusters
        self.wf = {'total':0, 'success':0, 'fail':0, 'success_dur':0,
                    'fail_dur':0}
        Method.__init__(self, src, sink)
        pass

    def process(self, item):
        """process one jobstate event
        Returns: current workflow object with current classification
        """
        if(item[1]['event']=='stampede.workflow.start'):
            self.handleWf(item[0],item[1])
        if(item[1]['event']=='stampede.job.state'):
            try:
                r = self.stateMap[item[1]['state']](item[0], item[1])
                return [(r)]
            finally:
                pass
        #return " "
    
    def noop(self, ts, record):
        #return " "
        pass

    def handleWf(self, ts, record):
        self.wf['ts'] = ts
        self.wf['id'] = record['wf.id']

    def handleSubmit(self, ts, record):
        self.jobInfo[record['job.id']] = {}
        self.jobInfo[record['job.id']]['tsubmit'] = ts
        self.wf['total'] = self.wf['total']+1
        #return " "
        pass

    def handleExecute(self, ts, record):
        self.jobInfo[record['job.id']]['delay'] = ts - self.jobInfo[record['job.id']]['tsubmit']
        self.jobInfo[record['job.id']]['texec'] = ts
        #return " "
        pass

    def handleSuccess(self, ts, record):
        try:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['texec']
        except:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['tsubmit']
        self.wf['success_dur'] = (float(self.wf['success']) * float(self.wf['success_dur']) + float(self.jobInfo[record['job.id']]['duration']))/(float(self.wf['success'])+1)
        self.wf['success'] = self.wf['success'] + 1
        cur = {}
        cur['total'] = float(self.wf['success']+self.wf['fail'])/self.wf['total']
        cur['success'] = float(self.wf['success'])/self.wf['total']
        cur['fail'] = float(self.wf['fail'])/self.wf['total']
        cur['success_dur'] = self.wf['success_dur']/float(ts-self.wf['ts'])
        cur['fail_dur'] = self.wf['fail_dur']/float(ts-self.wf['ts'])
        return (self.wf['id'], self.classify(cur), cur)
        pass

    def handleFailure(self, ts, record):
        #t = calendar.timegm(ts)
        try:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['texec']
        finally:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['tsubmit']
        self.wf['fail_dur'] = (float(self.wf['fail'])*float(self.wf['fail_dur']) + float(self.jobInfo[record['job.id']]['duration']))/(float(self.wf['fail'])+1)
        self.wf['fail'] = self.wf['fail'] + 1
        cur = {}
        cur['total'] = float(self.wf['success']+self.wf['fail'])/self.wf['total']
        cur['success'] = float(self.wf['success'])/self.wf['total']
        cur['fail'] = float(self.wf['fail'])/self.wf['total']
        cur['success_dur'] = self.wf['success_dur']/float(ts-self.wf['ts'])
        cur['fail_dur'] = self.wf['fail_dur']/float(ts-self.wf['ts'])
        return (self.wf['id'], self.classify(cur), cur)
        pass

    def handleAbort(self, ts, record):
       #return " "
       pass

    def classify(self, wf):
        #return the classification of the current workflow
        dis = distance(self.clusters[0], wf)
        idx = 0
        for i in (1, 2, 3):
            d =  distance(self.clusters[i], wf)
            if d < dis :
                dis = d
                idx = i
        return idx
        pass
