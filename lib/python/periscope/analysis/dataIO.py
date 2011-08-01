
from _base import DataSource
from _base import DataSink

import threading
import time
import calendar
import Queue


class eventProducer(threading.Thread):
    def __init__(self, filename, q):
        """Initialization
        
        Args:
            filename - path to bp file
            q - Queue.PriorityQueue
        """
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
        self.eventQ.put((time.time(), None))
    pass

class eventQueue(DataSource, threading.Thread):
    def __init__(self, q):
        self.eventQ = q
        threading.Thread.__init__(self)
    
        
    def next(self):
        #while (True):
        e = self.eventQ.get()
        if e[1] is None:
            self.eventQ.task_done()
            raise StopIteration
            #break
        return e
        #if _debug==True :
        #    print "consumed event"
        #    print e

class FileProcessor(DataSource):
    """Class to encapsulate reading bp files into PriorityQueue
    """
    def __init__(self, filenames, m):
        self.Q = Queue.PriorityQueue(m)
        p={}
        n = len(filenames)
        
        for i in xrange(n):
            try:
                f = open(filenames[i])
                f.close()
                p[i] = eventProducer(filenames[i], self.Q)
                p[i].start()
            except:
                break
        self.events = eventQueue(self.Q)
        self.events.start()
    
    def next(self):
        return self.events.next()

class printOutput(DataSink):
    def put(self, item):
        """Put data item.

        """
        if item is not None:
            print item
