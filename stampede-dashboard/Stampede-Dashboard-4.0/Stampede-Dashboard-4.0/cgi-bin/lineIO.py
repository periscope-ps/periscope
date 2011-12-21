import calendar
import json
import re
import sys
import threading
import time

from _base import DataSink
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "ahmad"
__date__ = "$Aug 15, 2011 12:24:39 AM$"

class JsonOutput(DataSink):
    """
    Saves data items to .json file.
    """
    def __init__(self, filename):
        """Initialization.

        Args:
            filename: path to .json file.
        """
        self.out = open(filename, 'wb')

    def put(self, item):
        """Adds item to file, Json formated.

        Args:
            item: sequence of items; list, vector, dictionary...
        """
        if item is not None:
            # Uncomment for Pretty Json
            #self.out.write(json.dumps(item[1], sort_keys=False, indent=4))

            # Uncomment for ugly Json
            self.out.write(json.dumps(item[1], separators=(',', ':')))
        self.out.write("\n")

    def __del__(self):
        self.out.close()

class LineProducer(threading.Thread):
    """Line generator from a single .bp file.

    Attributes:
        eventQ: Queue.PriorityQueue, stores events ordered by timestamp

    """

    def __init__(self, q):
        """Initialization.

        Args:
            q: Queue.PriorityQueue to store the events in order by timestamp
        """

        self.eventQ = q
        threading.Thread.__init__(self)

    @staticmethod
    def parse_line(self, line):
        """
        Args:
            line: netlogger event string.

        Returns:
            A dictionary of event components.

        Notes:
            This function is made static due to the need in newSend.py.
        """
        d = {}

        # Handling the "argv" and its corresponding value
        pat = re.search(" argv=\".*\"", line)
        # Note the regular expression we search for in the line!
        if pat:
        # "res" is the matching string.
            res = pat.group(0)
            # Inserting the "argv" value into the dictionary.
            d["argv"] = res[7:-1].strip()
            # Cleaning up the mess.
            line = line.replace(res, "")[:-1]

        splits = line.split(' ')
        for s in splits:
            ss = s.partition('=')
            d[ss[0]] = ss[2]
        return(d)

    def run(self, d):
        """Start the thread.

        This re-defined 'run' function takes a dictionary 'd' and places it
        into the priority queue.
        """

        try:
            # Fraction of seconds in sorting is ignored
            t = time.strptime(d['ts'], r'%Y-%m-%dT%H:%M:%S.%fZ')
            self.eventQ.put((calendar.timegm(t), d))
        except:
            print "Unexpected error:", sys.exc_info(),
            print d
        self.eventQ.put((time.time(), None))

