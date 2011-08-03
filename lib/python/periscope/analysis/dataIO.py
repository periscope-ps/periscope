"""
IO classes for stampede online analysis.

Author:   Taghrid Samak <tsamak@lbl.gov>
Modified: $Id$
"""

import csv
import calendar
import Queue
import time
import threading

from _base import DataSink
from _base import DataSource

class EventProducer(threading.Thread):
    """Event generator from a single .bp file.
    
    Attributes:
        filename: .bp file
        eventQ: Queue.PriorityQueue, stores events ordered by 
        timestamp
    
    Usage:
        maxSize = sys.argv[1]
        filename = sys.argv[2]
        q = Queue.PriorityQueue(maxSize)
        events = eventProducer(filename, q)
        events.start()
        while (1):
            e = q.get()
            if e[1] is None:
                q.task_done()
                break
    """

    def __init__(self, filename, q):
        """Initialization.
        
        Args:
            filename: path to .bp file
            q: Queue.PriorityQueue to store the events in order by timestamp
        """

        if filename is not None:
            try:
                self.filename = filename
                f = open(filename)
                f.close()
            except:
                # TODO: handling file exceptions.
                pass
        self.eventQ = q
        threading.Thread.__init__(self)

    def __del__ (self):
        self.f.close()

    def read_line(self):
        """Generator to read lines from files.
        """
        self.f = open(self.filename)
        for line in self.f:
            yield self.parse_line(line)

    def parse_line(self, line):
        """Return dictionary of netlogger.
        
        Args:
            line: netlogger event string.
        
        Returns:
            A dictionary of event components.
        """
        d = {}
        splits = line.split(' ')
        for s in splits:
            ss = s.partition('=')
            d[ss[0]]=ss[2]
        return(d)

    def run(self):
        """Start the thread.
        
        The main loop reads each line in the input file, 
        extracts time stamp, and pushes the event into the priority 
        queue base on timestamp.
        """
        for d in self.read_line():
            #insert event in heap
            try:
                t = time.strptime(d['ts'],r'%Y-%m-%dT%H:%M:%S.000000Z')
                self.eventQ.put((calendar.timegm(t), d))
            except:
                print d
        self.eventQ.put((time.time(), None))
    pass

class EventQueue(DataSource, threading.Thread):
    """Generator to encapsulate the priority queue.
    
    Attributes:
        eventQ: Queue.PriorityQueue
    """

    def __init__(self, q):
        self.eventQ = q
        threading.Thread.__init__(self)
    
    def next(self):
        e = self.eventQ.get()
        if e[1] is None:
            self.eventQ.task_done()
            raise StopIteration
        return e

class FileProcessor(DataSource):
    """Class to process multiple .bp files.
    Creates a thread to read from each file, and insert netlogger 
    events to a priority queue.
    
    Usage:
        maxSize = sys.argv[1]
        filenames = sys.argv[2:]
        events = FileProcessor(filenames, maxSize)
        for e in events:
            process e
    """
    def __init__(self, filenames, m):
        """Initialization.
        
        Args:
            filenames: list of strings, path to files
            m: maximum queue size
        """
        
        self.Q = Queue.PriorityQueue(m)
        p={}
        n = len(filenames)
        
        for i in xrange(n):
            try:
                f = open(filenames[i])
                f.close()
                p[i] = EventProducer(filenames[i], self.Q)
                p[i].start()
            except:
                break
        self.events = EventQueue(self.Q)
        self.events.start()
    
    def next(self):
        return self.events.next()

class PrintOutput(DataSink):
    def put(self, item):
        """Prints item to stdio
        """

        if item is not None:
            print item
            
class CsvOutput(DataSink):
    """Saves data items to .csv file.
    """
    
    def __init__(self, filename):
        """Initialization.
        
        Args:
            filename: path to .csv file.
        """
        self.out = csv.writer(open(filename, 'wb'))
    
    def put(self, item):
        """Adds item to file, comma separated.
        
        Args: 
            item: sequence of items; list, vector, dictionary...
        """
        if item is not None:
            self.out.writerow(item)
