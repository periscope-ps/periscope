#!/usr/bin/env python
"""
Given x,y,z MIDs, dump the data values in range a to b to a CSV
"""
import argparse
import os
import sys
#
import pymongo
# pymongo_mr
#    git clone https://bitbucket.org/dangunter/pymongo_mr.git
try:
    from pymongo_mr import base as mr_base
except ImportError:
    print("ERROR: Required module 'pymongo_mr' is not installed or not in path.\n"
          "To get it: \n"
          "    git clone https://bitbucket.org/dangunter/pymongo_mr.git\n")
    sys.exit(1)

META_COLLECTION = "meta"
DATA_COLLECTION = "data"
    
def main(db=None, host=None, val_range=None, mids=None,
         ofile=None):
    m_conn = pymongo.Connection(host)
    m_db = m_conn[db]
    m_data = m_db[DATA_COLLECTION]
    def extract_range(doc):
        #print("@@extract_range "+str(doc))
        values = [ ]
        for v in doc['values']:
            if val_range[0] <= v[1] <= val_range[1]:
                values.append(v)
        if values:
            return { 'mid' : doc['mid'],
                     'values' : values }
        else:
            return None
    def my_mapper(doc):
        return doc['mid']
    #print("@@MIDS: "+str(mids))
    groups = mr_base.group(m_data,
        mapper=my_mapper,
        reducer=mr_base.reducer,
        filter={'mid': { '$in' : mids } },
        extractor = extract_range)
    # write csv
    ofile.write("key,timestamp,value\n")
    for k in groups:
        for obj in groups[k]:
            for v in obj['values']:
                ofile.write("{0},{1:f},{2:f}\n".format(k, v[0], v[1]))

if __name__ == "__main__":
    _finfo = sys.float_info
    desc = __doc__
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('mids', metavar='MID', type=str, nargs='+',
                        help='List of metadata ids')
    parser.add_argument('-i', '--stdin', action="store_true", dest="input",
                        help="Read additional MIDs from standard input")
    parser.add_argument("--db", metavar="DBNAME", type=str,
                        dest="dbname", default="test",
                        help="Mongo database name")
    parser.add_argument("--host", metavar="DBHOST", type=str,
                        dest="dbhost", default="localhost",
                        help="Mongo database host")
    parser.add_argument('--range', metavar='NUM', type=float, nargs=2,
                        dest="range", default=[_finfo.min, _finfo.max],
                        help='Pair of numbers specifying a range')
    args = parser.parse_args()

    # add mids from stdin, too
    all_mids = args.mids[:]
    if args.input:
        for line in sys.stdin:
            mo_mids = line.strip().split()
            all_mids.extend(mo_mids)

    main(db=args.dbname, host=args.dbhost, val_range=args.range,
         mids=all_mids, ofile=sys.stdout)
    
