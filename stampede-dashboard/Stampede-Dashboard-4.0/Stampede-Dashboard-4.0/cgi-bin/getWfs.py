#!/usr/bin/python
__author__="Hamdy"
__date__ ="$Oct 10, 2011 2:04:46 AM$"

import sys
import os
import json
from sys import argv
import time
import cgi

from netlogger.analysis.workflow import stampede_statistics as sstat
from sqlalchemy import create_engine

print "Content-Type: application/json\n\n"

form = cgi.FieldStorage()
db_name = form["db_name"].value
#Check if the passed database name exists in the same directory as our script:
file_exists = os.path.isfile(db_name+'.db')
if file_exists == True:
    db = 'sqlite:///'+ db_name +'.db'
    g_engine =  create_engine(db, echo=False)
    conn = g_engine.connect()
else:
    print ""
    sys.exit()


#This function queries for all the workflow uuid's (wf_uuid):
def get_all_workflows ():
    all_ids = {}
    q = "select wf_uuid from workflow"
    result = conn.execute(q)
    count = 1
    for row in result:
        all_ids[count] = str(row).strip("( ' , ) u")
        count += 1
    return all_ids

print json.dumps(get_all_workflows(),indent=2)
