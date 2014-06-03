"""
Distance-based classifier for stampede online analysis.

Author:   Taghrid Samak <tsamak@lbl.gov>
Modified: $Id$
"""

from _base import Method

def distance(x, y):
    """Squared, Euclidean distance between two vectors.
    """

    d=0
    for i in x:
        d = d + (x[i]-y[i]) * (x[i]-y[i])
    return d
    pass

class OnlineClassify(Method):
    """distance-based classifier.
    
    Attributes:
        job_info: list of jobs currently being processing, submit was 
        seen, but not yet terminated.
        state_map: functions to handle each jobstate events.
        event_map: functions to handle workflow events.
        clusters: list of clusters centers.
        wf: workflow object averaging all jobstate events so far.
    """
    
    def __init__(self, src, sink, clusters):
        """Initialize with data source and sink.

        Args:
            src: DataSource.
            sink: DataSink.
            clusters: list of maps with cluster centers.
        """
        self.job_info = {}
        self.state_map = {
            'SUBMIT': self.handle_submit,
            'EXECUTE': self.handle_execute,
            'JOB_SUCCESS': self.handle_success,
            'JOB_FAILURE': self.handle_failure,
            'JOB_ABORTED': self.handle_abort,
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
        self.event_map = {
            'stampede.workflow.plan' : self.handle_wf,
            'stampede.wrokflow.start' : self.handle_wf,
            'stampede.workflow.end' :self.handle_wf
        }

        self.clusters = clusters
        self.wf = {'total':0, 'success':0, 'fail':0, 'success_dur':0,
                    'fail_dur':0}
        Method.__init__(self, src, sink)
        pass

    def process(self, item):
        """process one jobstate event
        calls the appropriate handler for the event.
        
        Args:
            item: event with timestamp (ts, event)
        
        Returns: 
            A dictionary holding current workflow object with current 
            classification.
        """
        if(item[1]['event']=='stampede.workflow.start'):
            self.handle_wf(item[0],item[1])
        if(item[1]['event']=='stampede.job.state'):
            try:
                r = self.state_map[item[1]['state']](item[0], item[1])
                return [(r)]
            finally:
                pass
        #return " "
    
    def noop(self, ts, record):
        pass

    def handle_wf(self, ts, record):
        self.wf['ts'] = ts
        self.wf['id'] = record['wf.id']

    def handle_submit(self, ts, record):
        self.job_info[record['job.id']] = {}
        self.job_info[record['job.id']]['tsubmit'] = ts
        self.wf['total'] = self.wf['total']+1
        pass

    def handle_execute(self, ts, record):
        self.job_info[record['job.id']]['delay'] = ts - self.job_info[record['job.id']]['tsubmit']
        self.job_info[record['job.id']]['texec'] = ts
        pass

    def handle_success(self, ts, record):
        try:
            self.job_info[record['job.id']]['duration'] = ts - self.job_info[record['job.id']]['texec']
        except:
            self.job_info[record['job.id']]['duration'] = ts - self.job_info[record['job.id']]['tsubmit']
        self.wf['success_dur'] = (float(self.wf['success']) * float(self.wf['success_dur']) + float(self.job_info[record['job.id']]['duration']))/(float(self.wf['success'])+1)
        self.wf['success'] = self.wf['success'] + 1
        cur = {}
        cur['total'] = float(self.wf['success']+self.wf['fail'])/self.wf['total']
        cur['success'] = float(self.wf['success'])/self.wf['total']
        cur['fail'] = float(self.wf['fail'])/self.wf['total']
        cur['success_dur'] = self.wf['success_dur']/float(ts-self.wf['ts'])
        cur['fail_dur'] = self.wf['fail_dur']/float(ts-self.wf['ts'])
        return [self.wf['id'], cur, self.classify(cur)]
        pass

    def handle_failure(self, ts, record):
        try:
            self.job_info[record['job.id']]['duration'] = ts - self.job_info[record['job.id']]['texec']
        finally:
            self.job_info[record['job.id']]['duration'] = ts - self.job_info[record['job.id']]['tsubmit']
        self.wf['fail_dur'] = (float(self.wf['fail'])*float(self.wf['fail_dur']) + float(self.job_info[record['job.id']]['duration']))/(float(self.wf['fail'])+1)
        self.wf['fail'] = self.wf['fail'] + 1
        cur = {}
        cur['total'] = float(self.wf['success']+self.wf['fail'])/self.wf['total']
        cur['success'] = float(self.wf['success'])/self.wf['total']
        cur['fail'] = float(self.wf['fail'])/self.wf['total']
        cur['success_dur'] = self.wf['success_dur']/float(ts-self.wf['ts'])
        cur['fail_dur'] = self.wf['fail_dur']/float(ts-self.wf['ts'])
        return [self.wf['id'], cur, self.classify(cur)]
        pass

    def handle_abort(self, ts, record):
       pass

    def classify(self, wf):
        """Returns workflow classification.
        The index of the nearest cluster is returned.
        
        Args:
            wf: workflow vector
        """
        dis = distance(self.clusters[0], wf)
        idx = 0
        for i in (1, 2, 3):
            d =  distance(self.clusters[i], wf)
            if d < dis :
                dis = d
                idx = i
        return idx
        pass
