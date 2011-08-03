"""
Online classification
Used for HPCC results
"""

__author__="taghrid"
__date__ ="$Apr 20, 2011 3:02:25 PM$"

import threading
import time
import calendar

import Queue


_debug = False

def distance(x, y):
    d=0
    for i in x:
        d = d + (x[i]-y[i]) * (x[i]-y[i])
    return d
    pass

class eventProducer(threading.Thread):
    def __init__(self, filename, q):
        #self.filter = event
        if filename is not None:
            try:
                self.filename = filename
                f = open(filename)
                f.close()
            except:
                pass
        self.eventQ = q
        threading.Thread.__init__(self)

    def __del__ (self):
        self.f.close()

    def readLine(self):
        self.f = open(self.filename)
        for line in self.f:
            yield self.parseLine(line)

    def parseLine(self, line):
        d = {}
        splits = line.split(' ')
        for s in splits:
            ss = s.partition('=')
            d[ss[0]]=ss[2]
        return(d)

    def run(self):
        for d in self.readLine():
            #insert event in heap
            try:
                t = time.strptime(d['ts'],r'%Y-%m-%dT%H:%M:%S.000000Z')
                self.eventQ.put((calendar.timegm(t), d))
            except:
                print d
            if _debug==True :
                print "produced event"
                print d
        self.eventQ.put((time.time(), None))
    pass

class onlineClassify(threading.Thread):
    def __init__(self, clusters, q):

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
        self.eventQ = q
        threading.Thread.__init__(self)
        pass

    def run(self):
        while (True):
            e = self.eventQ.get()
            if e[1] is None:
                break
            r = self.processEvent(e)
            if r is not None :
                print self.wf['id'], e[1]['ts'], r
            self.eventQ.task_done()
            if _debug==True :
                print "consumed event"
                print e

    def processEvent(self, e):
        if _debug==True:
            print e
        if(e[1]['event']=='stampede.workflow.start'):
            self.handleWf(e[0],e[1])
        if(e[1]['event']=='stampede.job.state'):
            try:
                r = self.stateMap[e[1]['state']](e[0], e[1])
                return r
            finally:
                pass

    def noop(self, ts, record):
        pass

    def handleWf(self, ts, record):
        self.wf['ts'] = ts
        self.wf['id'] = record['wf.id']

    def handleSubmit(self, ts, record):
        self.jobInfo[record['job.id']] = {}
        self.jobInfo[record['job.id']]['tsubmit'] = ts
        self.wf['total'] = self.wf['total']+1
        if _debug==True :
            print "inside submit"
            print record
            print self.wf
        #return ('Submit', self.wf)
        pass

    def handleExecute(self, ts, record):
        if _debug==1 : print record
        self.jobInfo[record['job.id']]['delay'] = ts - self.jobInfo[record['job.id']]['tsubmit']
        self.jobInfo[record['job.id']]['texec'] = ts
        if _debug==True :
            print "inside execute"
            print record
            print self.wf
        #return ('Execute', self.wf)
        pass

    def handleSuccess(self, ts, record):
        if _debug==True : print record
        try:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['texec']
        except:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['tsubmit']
        self.wf['success_dur'] = (float(self.wf['success']) * float(self.wf['success_dur']) + float(self.jobInfo[record['job.id']]['duration']))/(float(self.wf['success'])+1)
        self.wf['success'] = self.wf['success'] + 1
        if _debug==True :
            print "inside success"
            print record
            print self.wf
        cur = {}
        cur['total'] = float(self.wf['success']+self.wf['fail'])/self.wf['total']
        cur['success'] = float(self.wf['success'])/self.wf['total']
        cur['fail'] = float(self.wf['fail'])/self.wf['total']
        cur['success_dur'] = self.wf['success_dur']/float(ts-self.wf['ts'])
        cur['fail_dur'] = self.wf['fail_dur']/float(ts-self.wf['ts'])
        return (self.classify(cur), cur)
        pass

    def handleFailure(self, ts, record):
        if _debug==True : print record
        #t = calendar.timegm(ts)
        try:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['texec']
        finally:
            self.jobInfo[record['job.id']]['duration'] = ts - self.jobInfo[record['job.id']]['tsubmit']
        self.wf['fail_dur'] = (float(self.wf['fail'])*float(self.wf['fail_dur']) + float(self.jobInfo[record['job.id']]['duration']))/(float(self.wf['fail'])+1)
        self.wf['fail'] = self.wf['fail'] + 1
        if _debug==True :
            print "inside fail"
            print record
            print self.wf
        cur = {}
        cur['total'] = float(self.wf['success']+self.wf['fail'])/self.wf['total']
        cur['success'] = float(self.wf['success'])/self.wf['total']
        cur['fail'] = float(self.wf['fail'])/self.wf['total']
        cur['success_dur'] = self.wf['success_dur']/float(ts-self.wf['ts'])
        cur['fail_dur'] = self.wf['fail_dur']/float(ts-self.wf['ts'])
        return (self.classify(cur), cur)
        pass

    def handleAbort(self, ts, record):
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

    def cluster(self):
        pass

class proxy(threading.Thread):
    def __init__(self, clusters, q, m):
        #self.filter = event
        self.eventQ = q
        self.max_size = m
        self.clusters = clusters
        threading.Thread.__init__(self)
        
    def run(self):
        qs = {}
        cs = {}
        while (True):
            e = self.eventQ.get()
            if e[1] is None:
                break
            wf = e[1]['wf.id']
            if not (wf in qs):
                if _debug==True :
                    print "create consumer thread"
                    print wf
                qs[wf] = Queue.PriorityQueue(self.max_size)
                cs[wf] = onlineClassify(self.clusters, qs[wf])
                cs[wf].start()
            qs[wf].put(e)

            self.eventQ.task_done()
            if _debug==True :
                print "consumed event"
                print e
        for k in qs:
            qs[k].put((time.time(), None))


def main():
    """shared variable Heap
    producer is eventReader, fills Heap
    in the future, producer will read from message bus and fills Heap
    consumer is analysis process, reads Heap
    """
    import sys
    app = sys.argv[1]
    filename = sys.argv[2]

    clusters = getClusters(app)

    Q = Queue.PriorityQueue()

    p = eventProducer(filename, Q)
    p.start()

    c = onlineClassify(clusters, Q)
    c.start()
    

if __name__ == "__main__":
    main()
