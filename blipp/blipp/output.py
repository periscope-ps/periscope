"""
Output classes and functions.

Author: Dan Gunter <dkgunter@lbl.gov>
"""
import logging
import sys

import simplejson as json

from blipp.util import bson_decode, log_formatter

class SinkException(Exception):
    pass

class Sink:
    def __init__(self, encode_fn=None):
        self._encode = encode_fn
        self.log = logging.getLogger("blipp.output.sink")
        
    def add(self, data):
        pass
    def close(self):
        pass
    
class XSP_sink(Sink):
    def __init__(self, host, port):
        self.log.debug("xsp_connect.start")
        try:
            self.xsp_sess = xsplib.XSPSession()
            self.xsp_sess.connect(host, port)
        except Exception, err:
            g_log.critical("xsp_connect.error, msg=%s host=%s, port=%d, details=%s",
                           "failed connection to xsp",
                           host, port, util.traceback())
            raise SinkException("XSP connect error")
        self.log.debug("xsp_connect.end, status=%d", status)
        
    def add(self, data):
        bsondata = bson_encode(data)
        self.xsp_sess.send_msg(data, len(data), XSP_TYPE)

    def close(self):
        try:
            self.xsp_sess.close()
        except socket.error, err:
            self.log.warn("xsp_close.failed, msg=%s", str(err))

class Print_sink(Sink):
    """Print data as JSON to standard output.
    """
    def add(self, data):
        json.dump(data, sys.stdout)

