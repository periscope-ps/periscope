"""
Basic Lightweight Periscope Probe (BLiPP)

This file implements the base functionality.
"""
__author__ = "Dan Gunter <dkgunter@lbl.gov>"
__rcsid__ = "$Id: base.py 27244 2011-02-25 20:16:55Z dang $"

# System imports
import logging
import uuid

## Constants and globals
## ---------------------

BLIPP_VERSION = (0,1)

SIOCGIFCONF = 0x8912

VERSION_FLD = 'version'
METAID_FLD = 'mid'
ID_FLD = 'id'
PARENT_ID_FLD = 'pid'

META_SECT = 'meta'
DATA_SECT = 'data'

g_log = None

## Classes and functions
## ---------------------

def init_logging():
    global g_log
    g_log = logging.getLogger("blipp.base")

class Session:
    def __init__(self):
        self._leaf_mblocks = { }
        self._block = None

    def set_block(self, block):
        self._block = block

    def get_meta_block(self, data_type, parent_meta):
        key = (parent_meta.ident, data_type)
        mblock = self._leaf_mblocks[key]
        return mblock

    def set_meta_block(self, data_type, parent_meta):
        key = (parent_meta.ident, data_type)
        mblock = MetaBlock(data_type=data_type, parent=parent_meta)
        self._block.meta.append(mblock)
        self._leaf_mblocks[key] = mblock.ident

class Block:
    version = '.'.join(map(str,BLIPP_VERSION))
    def __init__(self):
        self.clear()

    def clear(self):
        self.meta = [ ]
        self.clear_data()

    def clear_data(self):
        self._data = { }

    def add_data_block(self, d):
        """Add data block to the container.

        If there is already data section with the same
        metadata parent, then add this data to that
        section. Otherwise start a new section.
        """
        key = d.meta_id
        if not self._data.has_key(key):
            # new section
            self._data[key] = d
        else:
            # merge with existing section
            self._data[key].values.extend(d.values)

    def as_dict(self):
        d = { VERSION_FLD : self.version,
              META_SECT : [x.as_dict() for x in self.meta],
              DATA_SECT : [x.as_dict() for x in self._data.values()] }
        return d

class MetaBlock:
    def __init__(self, parent=None, event_type=None, subject={}, params={}, data_type=None):
        self.ident = str(uuid.uuid1())
        self.parent = parent
        self.event_type = event_type
        self.data_type = data_type
        self.subject = subject
        self.params = params

    def as_dict(self):
        d = { ID_FLD : self.ident,
              'subject' : self.subject,
              'params' : self.params }
        if self.event_type:
              d['type'] = self.event_type
        if self.parent:
            if hasattr(self.parent, 'ident'):
                d[PARENT_ID_FLD] = str(self.parent.ident)
            else:
                d[PARENT_ID_FLD] = str(self.parent)
        if self.data_type:
            d['event_type'] = self.data_type
        return d

    def __str__(self):
        return self.ident

class DataBlock:
    def __init__(self, meta=None):
        if hasattr(meta, 'ident'):
            self.meta_id = str(meta.ident)
        else:
            self.meta_id = str(meta)
        self.values = [ ]

    def add_value(self, timestamp, value):
        self.values.append([timestamp, value])

    def as_dict(self):
        d = { #ID_FLD : self.ident,
              METAID_FLD : self.meta_id,
              #'event_type' : self.event,
              'values' : self.values }
        return d

