"""
Base classes, etc. for Periscope analysis modules.

Author:   Dan Gunter <dkgunter@lbl.gov>
Modified: $Id$
"""

import time

# Skeleton classes

class DataSource:
    """Generic data source.
    May be a file, database, message bus, etc.
    """
    def next(self):
        """Get next data item.

        Returns:
          One data item. If the item is None, then the caller
          should understand that there is no more data now, but may be later.
        Raises:
          StopIteration - no more data, ever
        """
        raise StopIteration

    def __iter__(self):
        return self

class DataSink:
    """Generic data sink.
    May be a file, database, message bus, etc.
    """
    def put(self, item):
        """Put data item.

        Returns: None
        """
        return None

class Method:
    """Generic analysis algorithm.
    """
    def __init__(self, src, sink):
        """Initialize with data source and sink.

        Args:
          src - Obj supporting DataSource interface.
          sink - Obj supporting DataSink interface.
        """
        self._src, self._sink = src, sink

    def process(self, item):
        """Override this method with logic to handle an item.

        Returns: list of result objects
        """
        return [ ]
    
    def run(self, max_items=0, max_time=0):
        """Process a batch of items.
        If max_items and max_time are both 0, then
        this will run until there is no more input.
        
        Args:
          max_items - Max #items to process, 0=infinite.
          max_time - Max time (sec) to spend, 0=infinite.
        """
        n, t0 = 0, time.time()
        while 1:
            try:
                item = self._src.next()
            except StopIteration:
                break
            if item is None: # no result, but don't stop
                time.sleep(0.1)
                continue
            results = self.process(item)
            if results is None :
                continue
            for r in results:
                self._sink.put(r)
            if max_items > 0:
                n += 1
                if n >= max_items:
                    break
            if max_time > 0:
                t1 = time.time()
                if t1 - t0 >= max_time:
                    break
