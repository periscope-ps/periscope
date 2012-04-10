#!/usr/bin/env python
"""
Flatten Periscope data.
"""
import argparse
import os
import pprint
import sys
#
import pymongo

def kvp_str(ddict, sep=';'):
    dlist = [k + '=' + str(v) for k,v in ddict.items()]
    return sep.join(dlist)

def unchain(meta, mid):
    """Walk up the metadata chain.
    """
    type_ = None
    subj_list, param_list = [ ], [ ]
    while mid is not None:
        mrec = meta.find_one({'id':mid})
        if mrec is None:
            raise KeyError("Missing mid: {}".format(mid))
        if type_ is None:
            try:
                type_ = mrec['type']
            except KeyError:
                type_ = mrec['event_type']
        if mrec['subject']:
            subj_list.insert(0, kvp_str(mrec['subject']) )
        else:
            subj_list.insert(0, "")
        if mrec['params']:
            param_list.insert(0, kvp_str(mrec['params']))
        else:
            param_list.insert(0, "")
        mid = mrec.get('pid', None)
    return type_, subj_list, param_list

def to_csv(db, ofile):
    """Write to CSV.
    """
    mids = { }
    data = db.data
    meta = db.meta
    ofile.write("key,type,subject,param,timestamp,value\n")
    for rec in data.find():
        # Pull out cached metadata
        mid = rec['mid']
        type_, subj, param = mids.get(mid, (None, None, None))
        # If not found, get new string-ified metadata for this mid
        if type_ is None:
            type_, subj_list, param_list = unchain(meta, mid)
            subj = '/'.join(subj_list)
            param = '/'.join(param_list)
            mids[mid] = (type_, subj, param)
        # Print flattened record for each value
        for v in rec['values']:
            ofile.write('{key},{type},"{subj}","{param}",{timestamp},{value}\n'.
                    format(key=mid, type=type_, subj=subj, param=param,
                           timestamp=v[0], value=v[1]))

def main(db=None, host=None, ofile=None):
    """Program.
    """
    m_conn = pymongo.Connection(host)
    to_csv(m_conn[db], ofile)

if __name__ == "__main__":
    _finfo = sys.float_info
    desc = __doc__
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--db", metavar="DBNAME", type=str,
                        dest="dbname", default="test",
                        help="Mongo database name")
    parser.add_argument("--host", metavar="DBHOST", type=str,
                        dest="dbhost", default="localhost",
                        help="Mongo database host")
    args = parser.parse_args()

    main(db=args.dbname, host=args.dbhost, ofile=sys.stdout)
