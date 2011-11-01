#!/usr/bin/python
__author__="Hamdy"
__date__ ="$Oct 10, 2011 2:04:46 AM$"
import json
import sys
from sys import argv
import time

import cgi
from netlogger.analysis.workflow import stampede_statistics as sstat
import os
from sqlalchemy import create_engine

print "Content-Type: application/json\n\n"

#Zakaria.start
form = cgi.FieldStorage()
key = form["key"].value
#Zakaria.end

#Initializing all we need for connecting to the database:

#Obtain database name via CGI arguments.
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

#This type statistics dictionary stores statistics for:
#job type : {successful instances: (initialized to 0),
#failing instances: (initialized to 0)}
type_stats = {}

#Valid Pegasus Job Types (string types).
#Taken from a .yang downloaded from: http://goo.gl/1L0Bv
type_list = ["unknown", "compute","stage_in_tx","stage_out_tx","registration",
           "inter_site_tx","create_dir","staged_compute","cleanup","chmod","dax","dag"]


#A function to initialize our type statistics dictionary (type_stats).
#Called from main on the type list (type_list).
def initialize_dict(type,type_stats):
    type_stats[type] = {}
    type_stats[type]['successful'] = 0
    type_stats[type]['fail'] = 0

#Get a corresponding wf_id for the wf_uuid:
def get_wf_id (wf_uuid):
    q = "select wf_id from workflow where wf_uuid = '" + wf_uuid + "'"
    result = conn.execute(q)
    return str(result.fetchone()).strip("( , )")


#This functions checks for each job_id if it has at least 1 job_instance_id or not.
#If it does, record this as a valid job_id. Populate job types dictionary with
#(valid) job_ids : types.
def get_valid_job_ids (wf_id, job_types):
    q = "select job_id,type_desc from job where wf_id = " + wf_id + " order by job_id asc"
    result = conn.execute(q)

    #This dictionary contains all job_ids that have one or more corresponding job_instance_ids.
    #counter for looping purposes.
    valid_job_ids = {}
    counter = 0

    for row in result:
        #Count for each job id how many job_instance_ids there are:
        q = "select count(*) from job_instance where job_id = " + str(row[0]).strip("( , )")
        result_in = conn.execute(q)
        for row_in in result_in:
            #Check if the returned row was not empty:
            if str(row_in[0]).strip("( , )") != "0":
                valid_job_ids[counter] = str(row[0]).strip("( , )")

                job_types[str(row[0]).strip("( , )")] = (str(row[1]).strip("( , )")).replace("-","_")
                counter += 1
            else:
                pass
    return valid_job_ids

#This function gets passed a unique workflow id (wf_uuid).
#It populates the type statistics (type_stats)
#dictionary and returns a timestamp statistics (timestamp_stats) dictionary that stores:
#valid job id : {status:[0 for success, -1 for failure], timestamp of status [seconds from epoch]}
def get_wf_stats (wf_uuid):
    #Start by getting the wf_id:
    wf_id = get_wf_id(wf_uuid)

    #Now get all the job_ids that correspond to this wf_id and have one or more job instances:
    #This dictionary stores:
    #(valid)job_id : type_desc
    job_types = {}

    #This dictionary stores:
    #arbitary counter : (valid) job_id
    valid_job_ids = get_valid_job_ids(wf_id,job_types)

    #This dictionary stores:
    #valid job id : {status:[0 or -1], timestamp [seconds from epoch]}
    timestamp_stats = {}

    #Get job_instance_ids for each of the valid job_ids:
    for key in valid_job_ids:
        q = "select job_instance_id from job_instance where job_id = "+valid_job_ids[key]
        result = conn.execute(q)
        status = get_job_status(result)
        if status['status'] == 0:
            type_stats[job_types[valid_job_ids[key]]]['successful'] += 1
        elif status['status'] == -1:
            type_stats[job_types[valid_job_ids[key]]]['fail'] += 1
        timestamp_stats[valid_job_ids[key]] = {}
        timestamp_stats[valid_job_ids[key]] = status
    return timestamp_stats


#Take in a returned row of job instances (ResultProxy object), find if any of them failed.
#Record each failure and each success against its timestamp.
#Return a dictionary of:
#status : timestamp
def get_job_status(result):
    status_timestamp = {}
    for row in result:
        job_instance_id = str(row[0]).strip("( , )")
        q_1 = "select job_instance_id,state,timestamp from jobstate where job_instance_id = "
        q_2 = " and (state = 'JOB_SUCCESS' or state = 'JOB_FAILURE' )"
        q = q_1 + job_instance_id + q_2
        result_in = conn.execute(q)
        for row_in in result_in:
            if str(row_in[1]).strip("( , )") == "JOB_FAILURE":
                status_timestamp['status'] = -1
            else:
                status_timestamp['status'] = 0
        status_timestamp['timestamp'] = str(row_in[2]).strip("( , )")
        #if status_timestamp['status'] == None:
            #status_timestamp['status'] = -1
    return status_timestamp


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

#This function takes an input id (a workflow id, wf_id) and uses the statistics API
#to get summaries, records it in the search_results dictionary and returns the dictionary.
def get_api_summaries(input_id):
    search_results = {}
    q = "select wf_id, wf_uuid, dax_label from workflow where wf_uuid = '" + str(input_id)+"'"
    result = conn.execute(q)
    for row in result:
        stats = sstat.StampedeStatistics(db, True)
        stats.set_job_filter('all')
        stats.initialize(row.wf_uuid)
        wf_details = stats.get_workflow_details()
        for row in wf_details:
            search_results["wf_id"] = row.wf_id
            search_results["dax_label"] = row.dax_label
            search_results["root_wf_id"] = row.root_wf_id
        wf_states = stats.get_workflow_states()

        count = 0
        for row in wf_states:
            if count == 0:
                search_results["start_state"] = row.state
                search_results["start_timestamp"] = time.ctime(row.timestamp)
                count += 1
            else:
                search_results["end_state"] = row.state
                search_results["end_timestamp"] = time.ctime(row.timestamp)
    return search_results


#This checks if the id passed is valid:
def bad_id(id):
    q = "select count(*) from workflow where wf_uuid = '"+id+"'"
    result = conn.execute(q)
    if str(result.fetchone()).strip("( , )") != "1":
        return -1
    else:
        return 0

#This function accumulates total statistics of successful and failing jobs
#regardless of job type. Returns a dictionary of:
#{successful: (initialized to 0), failing: (initialized to 0)}
def get_totals(type_stats):
    totals = {}
    totals['successful'] = 0
    totals['failing'] = 0
    for key in type_stats:
        totals['successful'] += type_stats[key]['successful']
        totals['failing'] += type_stats[key]['fail']
    return totals

def get_timestamp_list(dict):
    ts_list = []
    for key in dict:
        if dict[key]['timestamp'] in ts_list:
            pass
        else:
            ts_list.append(dict[key]['timestamp'])
    return ts_list

def get_timeseries_data(ts_dict,ts_list):
    ts_data = {}
    for ts in ts_list:
        ts_data[ts] = {}
        ts_data[ts]['successful'] = 0
        ts_data[ts]['fail'] = 0
        for key in ts_dict:
            if ts_dict[key]['timestamp'] == ts:
                if (ts_dict[key]['status']== 0):
                    ts_data[ts]['successful'] += 1
                else:
                    ts_data[ts]['fail'] += 1
    return ts_data

def format_timeseries_data(timeseries_data):
    timeseries_fmted = []
    
    for key in timeseries_data:
        loop_dict = {}
        loop_dict['timestamp'] = key
        loop_dict['successful'] = timeseries_data[key]['successful']
        loop_dict['fail'] = timeseries_data[key]['fail']
        timeseries_fmted.append(loop_dict)
    return timeseries_fmted

for type in type_list:
    initialize_dict(type,type_stats)

input = key
#Sample inputs:
#c44617de-b480-45dd-86ad-6f4ef9be504e-90
#c44617de-b480-45dd-86ad-6f4ef9be504e
#c44617de-b480-45dd-86ad-6f4ef9be504e
#or any other available unique workflow ID.
if not bad_id(input):
    json_result = {}


    #Time-series statistics:
    timestamps_status = get_wf_stats(input)
    timestamps_list = get_timestamp_list(timestamps_status)
    timeseries_data = get_timeseries_data(timestamps_status,timestamps_list)
    timeseries_fmted = format_timeseries_data(timeseries_data)

    json_result['api_summaries'] = get_api_summaries(input)
    json_result['timeseries_data'] = timeseries_fmted
    json_result ['type_statistics'] = type_stats
    json_result['totals'] = get_totals(type_stats)

    print json.dumps(json_result,indent=2)
else:
    print ""
    sys.exit()
