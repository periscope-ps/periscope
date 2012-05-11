"""
Database helpers for web back-end
"""
__rcsid__ = "$Id: db.py 30872 2012-03-09 23:21:47Z davidr $"

import sqlalchemy as sa
import time
from datetime import datetime
from netlogger.analysis.workflow import stampede_statistics as sstat

class StampedeDB:
    def __init__(self, url):
        self.engine = sa.create_engine(url)
        self.dburl = url
	self.status_mapping = {
	    'WORKFLOW_STARTED': 'Running',
	    'WORKFLOW_TERMINATED': 'Done'
	}

    def _connect(self):
        return self.engine.connect()

    def get_max_ts(self):
        result = 0.0
        conn = self._connect()
        try:
            qstr = "select max(timestamp) as 'ts' from jobstate"        
            result = float(conn.execute(qstr).first()[0])
        except sa.exc.SQLAlchemyError, err:
            pass #XXX: should do *something*
        return result

    def find_root_workflows(self):
        conn = self._connect()
        results = []
        q = "select wf_id, wf_uuid, root_wf_id, dax_label from workflow"
        result = conn.execute(q)
        for row in result:
            if row.wf_id != row.root_wf_id: # only get top level workflows
	        continue
	    rowInfo = {}
	    rowInfo['id'] = row.wf_uuid
	    cell = []
	    cell.append(row.dax_label)
	    # don't expand workflows
            stats = sstat.StampedeStatistics(connString=self.dburl, expand_workflow=False)
            stats.set_job_filter('all')
            stats.initialize(row.wf_uuid)
            wf_states = stats.get_workflow_states()
            try:
                t = time.ctime(wf_states[0].timestamp)
            except IndexError:
                t = time.ctime(time.time())
            parsed = time.strptime(t)
            dtime = time.strftime("%b %e, %Y", parsed)
            cell.append(dtime)
	    if len(wf_states) > 1:
		row = wf_states[len(wf_states)-1]
		if row.status and (row.status == 1):
		    cell.append("Failed")
		else:
                    cell.append(self.status_mapping[row.state])
                t = time.ctime(row.timestamp)
                parsed = time.strptime(t)
                dtime = time.strftime("%b %e, %Y", parsed)
                cell.append(dtime)
	    else:
		cell.append("Running")
		cell.append("")
	    rowInfo['cell'] = cell
            results.append(rowInfo)
        return results

    def find_sub_workflows(self, parent_uuid):
        # Get list of all sub-workflows
        conn = self._connect()
        stats = sstat.StampedeStatistics(connString=self.dburl, expand_workflow=False)
        stats.initialize(parent_uuid)
        stats.set_job_filter('all')
	result = stats.get_sub_workflow_ids()
        successseries = []
        failureseries = []
        incompleteseries = []
        wfnames = []
        wfuuids = []
	totalSuccesses = 0
	totalFailures = 0
	totalIncompletes = 0
        # Build workflow summary info for each sub-workflow
        for wf_id, wf_uuid, label in result:
            stats = sstat.StampedeStatistics(connString=self.dburl, expand_workflow=False)
            stats.initialize(wf_uuid)
            stats.set_job_filter('all')
            total = stats.get_total_jobs_status()
            succ = stats.get_total_succeeded_jobs_status()
	    totalSuccesses += succ
            fail = stats.get_total_failed_jobs_status()
	    totalFailures += fail
	    successseries.append({'y': succ, 'uuid': wf_uuid})
	    failureseries.append({'y': fail, 'uuid': wf_uuid})
            if (total - succ - fail) > 0:
                incompleteseries.append({'y': total - succ - fail, 'uuid': wf_uuid})
		totalIncompletes += total - succ - fail
	    else:
                incompleteseries.append({'y': 0, 'uuid': wf_uuid})
            wfnames.append(label)
        results = {
            'successful' : successseries,
            'failed' : failureseries,
            'incomplete' : incompleteseries,
            'names' : wfnames
        }
        return results

    def find_workflow_stats(self, wf_uuid, includeSubTotals):
        conn = self._connect()
	if not includeSubTotals:
            stats = sstat.StampedeStatistics(connString=self.dburl, expand_workflow=False)
	else:
            stats = sstat.StampedeStatistics(connString=self.dburl, expand_workflow=True)
        stats.initialize(wf_uuid)
        stats.set_job_filter('all')
        jobTotal = stats.get_total_jobs_status()
        jobSuccesses = stats.get_total_succeeded_jobs_status()
        jobFailures = stats.get_total_failed_jobs_status()
        jobRetries = stats.get_total_jobs_retries()
        if (jobTotal - jobSuccesses - jobFailures) > 0:
            jobIncompletes = jobTotal - jobSuccesses - jobFailures
        else:
            jobIncompletes = 0
	xformSuccesses = 0
	xformFailures = 0
	xformIncompletes = 0
        xsuccessseries = []
        xfailureseries = []
        xincompleteseries = []
	xnames = []
	xforms = stats.get_transformation_statistics()
	for xform in xforms:
	    xformTotal = xform.count
	    if xformTotal != 0:
	        xnames.append(xform.transformation)
	        xsuccessseries.append(xform.success)
	        xformSuccesses += xform.success
	        xfailureseries.append(xform.failure)
	        xformFailures += xform.failure
	        incompletes = xformTotal - xform.success - xform.failure
                if (xformTotal - xform.success - xform.failure) > 0:
                    xformIncompletes += incompletes
		    xincompleteseries.append(incompletes)
	        else:
		    xincompleteseries.append(0)
	subSuccesses = 0
	subFailures = 0
	subIncompletes = 0
        taskTotal = stats.get_total_tasks_status()
        taskSuccesses = stats.get_total_succeeded_tasks_status()
        taskFailures = stats.get_total_failed_tasks_status()
        if (taskTotal - taskSuccesses - taskFailures) > 0:
            taskIncompletes = taskTotal - taskSuccesses - taskFailures
        else:
            taskIncompletes = 0
	result = stats.get_descendant_workflow_ids()
        # Get information for each sub-workflow
        for wf_id, wf_uuid in result:
            stats = sstat.StampedeStatistics(connString=self.dburl, expand_workflow=False)
            stats.initialize(wf_uuid)
            stats.set_job_filter('all')
            wf_states = stats.get_workflow_states()
	    if len(wf_states) > 1:
		row = wf_states[len(wf_states)-1]
		if row.status and (row.status == 1):
		    subFailures += 1
		elif row.state == 'WORKFLOW_STARTED':
                    subIncompletes += 1
	        elif row.state == 'WORKFLOW_TERMINATED':
                    subSuccesses += 1
	    else:
		#print("nothing returned for get_workflow_states")
		subIncompletes += 1
        results = {
	    'jobSuccesses': jobSuccesses,
	    'jobFailures': jobFailures,
	    'jobIncompletes': jobIncompletes,
	    'xformSuccesses': xformSuccesses,
	    'xformFailures': xformFailures,
	    'xformIncompletes': xformIncompletes,
	    'taskSuccesses': taskSuccesses,
	    'taskFailures': taskFailures,
	    'taskIncompletes': taskIncompletes,
	    'subSuccesses': subSuccesses,
	    'subFailures': subFailures,
	    'subIncompletes': subIncompletes,
            'names' : xnames,
            'xsuccessful' : xsuccessseries,
            'xfailed' : xfailureseries,
            'xincomplete' : xincompleteseries,
        }
        return results

