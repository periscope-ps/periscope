#!/usr/bin/env python
"""
Embedded REST server for dashboard
"""
__rcsid__ = "$Id$"

# System modules
from optparse import OptionParser
import json
import logging
import re
import sys
import time
import uuid
# Third-party modules
import web
# Local modules
from db import StampedeDB
import util

# shorthand for decorator
jsonic = util.returns_json

LOGGER_NAME = "st.analyzer"

class BadUUID(web.badrequest):
    message = "Bad UUID"

class Logged(object):
    def __init__(self):
        self.log = logging.getLogger(LOGGER_NAME)

class Index(Logged):
    def GET(self):
        return render.index()

class Database(Logged):
    """Return database information.
    """
    @jsonic
    def GET(self):
        result = {}
        result['name'] = web.ctx.dbname
        return result

class WfList(Logged):
    """List root workflows in a DB.
    """
    @jsonic
    def GET(self):
        db = web.ctx.db
        info = db.find_root_workflows()
        self.log.debug("get.wf.summ info={0}".format(info))
        result = {}
        result['page'] = '1'
        result['total'] = str(len(info))
        result['rows'] = info
        return result

class WfSummary(Logged):
    """Base class for getting workflow summaries.
    """
    def get_summary(self, path=[ ]):
        """Get summary, overridden in subclasses to
        get a more specific kind of summary.
        """
        # XXX: Get summary for wf at 'path'
        return { }

    @jsonic
    def GET(self, path):
        """Given a list of UUIDs as /-separated items
        in path, split them into a list then call
        get_summary() to get a summary of the
        selected workflow.

        Sub-classes can use this method and just
        override get_summary() to do something specific.
        """
        try:
            uuidlist = util.split_uuids(path)
        except ValueError, err:
            raise web.internalerror(err)
        self.db = web.ctx.db
        summ = self.get_summary(path)
        return summ

class WfSubList(WfSummary):

    def get_summary(self, path):
        self.log.info("get_summary.start")
        db = web.ctx.db
	results = db.find_sub_workflows(path)
	num = len(results['successful'])
	# not incorporating dax_label for now
        sub_names = ['{0:d}'.format(x) for x in range(1,num+1)]
	results['names'] = sub_names
	results['num'] = str(num)
        self.log.info("get_summary.end")
        return results

class WfInfo(WfSummary):
    def get_summary(self, path):
        self.log.info("info.get_summary.start")
	results = get_info(path, False)
        self.log.info("info.get_summary.end")
        return results

class WfSubInfo(WfSummary):
    def get_summary(self, path):
        self.log.info("subinfo.get_summary.start")
	results = get_info(path, True)
        self.log.info("subinfo.get_summary.end")
        return results

class WfTransforms(WfSummary):
    def get_summary(self, path):
        task_names = ['Transform 4', 'Transform 3', 'Transform 2', 'Transform 1']
        # faking results for now
        successseries = [30, 20, 60, 80]
        failureseries = [90, 10, 10, 50]
        incompleteseries = [100, 50, 10, 70]
        results = {
            'successful': successseries,
            'failed': failureseries,
            'incomplete': incompleteseries,
            'names': task_names,
            'num': str(len(task_names))
        }
        return results

class WfTasks(WfSummary):
    def get_summary(self, path):
        wfnames = ['Sub-workflows', 'Jobs', 'Transforms', 'Tasks']
        # faking results for now
        successseries = [50, 30, 40, 20]
        failureseries = [80, 30, 20, 50]
        incompleteseries = [0, 5, 10, 60]
        results = {
            'successful': successseries,
            'failed': failureseries,
            'incomplete': incompleteseries,
            'names': wfnames,
            'uuid': path,
            'num': 4
        }
        return results

class MockDB:
    """Mock database.
    """
    def find_workflows(self):
        return ['periodogram-123', 'cybershake-456']
    def get_max_ts(self):
        return 1328311499
    def find_root_workflows(self):
        return {
            'id': '1',
            'cell': ['gp', 'July 26, 2011', 'Done', 'July 27, 2011']
        }
    def find_sub_workflows(self):
        sub_names = ['{0:d}'.format(x) for x in range(1,11)]
	uuids = []
	for i in xrange(1,11):
	    indx = i % 10
	    uuids.append(path[0:len(path)-1] + str(indx))
	results = {
            'successful': [{'y': 30, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 20, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 60, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 80, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 50, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 40, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 20, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 30, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 10, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 80, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'}],
            'failed': [{'y': 90, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 10, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 10, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 50, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 20, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 70, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 40, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 10, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 90, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 30, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'}],
            'incomplete': [{'y': 100, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 50, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 10, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 70, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 20, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 90, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 80, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 50, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 10, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'},
            {'y': 60, 'uuid': '89a25dd1-e8ae-4f15-9dea-367bbf598779'}],
            'names': sub_names,
            'num': str(len(sub_names)),
            'uuids': uuids
        }
	return results

"""
URL patterns.
"""
urls = (
    '/', 'Index',              # Home page
    '/db', 'Database',
    '/wf/list', 'WfList',      # List of top-level workflows
    '/wf/(.*)/list', 'WfSubList',
    '/wf/(.*)/info', 'WfInfo', # summary info
    '/wf/(.*)/subinfo', 'WfSubInfo', # summary info including sub-workflows
    '/wf/(.*)/xfrm', 'WfTransforms', # Get transform summary
    '/wf/(.*)/task', 'WfTasks', # Get task/job summary
    )

"""
Set up main web app
"""

DB_URL = 'sqlite:///gp-0.stampede.db'

render = util.render("static/templates/")
app = web.application(urls, globals(), autoreload=True)

def main(test_only=False):
    """Main function For command-line usage
    """
    parser = OptionParser()
    parser.add_option("-t", "--test", action="store_true", dest="test_only")
    parser.add_option("-v", "--verbose", action="store_true", dest="vb")
    parser.add_option("-d", "--database", default=DB_URL, dest="dbname")
    (options, args) = parser.parse_args()
    print(options.dbname)
    sys.argv = sys.argv[:1] # reset for run()
    init_db(options.dbname, options.test_only)
    log = init_logging(debug=options.test_only or options.vb)
    log.info("app.run.start")
    app.run()
    log.info("app.run.end")

def init_db(dbname, test_only):
    """Initialize database for web.py usage.
    """
    # select database
    if test_only:
        db = MockDB()
    elif dbname:
        db = StampedeDB(dbname)
    # add processor for setting DB into context
    def load_stdb(handler):
        web.ctx.db = db
        web.ctx.dbname = dbname
        return handler()
    app.add_processor(load_stdb)

def get_info(uuid, includeSubTotals):
    results = {}
    wfnames = ['Tasks', 'Transforms', 'Jobs', 'Sub-workflows']
    db = web.ctx.db
    wf = db.find_workflow_stats(uuid, includeSubTotals)
    successseries = [wf['taskTotal'], wf['xformSuccesses'], wf['jobSuccesses'], wf['subSuccesses']]
    failureseries = [wf['taskTotal'], wf['xformFailures'], wf['jobFailures'], wf['subFailures']]
    incompleteseries = [wf['taskTotal'], wf['xformIncompletes'], wf['jobIncompletes'], wf['subIncompletes']]
    """
    successseries = [wf['taskuccesses'], wf['xformSuccesses'], wf['jobSuccesses'], wf['subSuccesses']]
    failureseries = [wf['taskFailures'], wf['xformFailures'], wf['jobFailures'], wf['subFailures']]
    incompleteseries = [wf['taskIncompletes'], wf['xformIncompletes'], wf['jobIncompletes'], wf['subIncompletes']]
    """
    task_results = {
        'successful': successseries,
        'failed': failureseries,
        'incomplete': incompleteseries,
        'names': wfnames,
        'uuid': uuid,
        'num': 4
    }
    results['summary'] = task_results
    num = len(wf['xsuccessful'])
    xform_results = {
        'successful': wf['xsuccessful'],
        'failed': wf['xfailed'],
        'incomplete': wf['xincomplete'],
        'names': wf['names'],
        'num': num
    }
    results['xforms'] = xform_results
    return results

class NLFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        """NetLogger's time format."""
        tm = time.gmtime(record.created)
        usec = int((record.created - int(record.created)) * 1e6)
        dt = "{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}".format(
                *tm[0:6])
        return "{0:s}.{1:06d}Z".format(dt, usec)

def init_logging(debug=False):
    log = logging.getLogger(LOGGER_NAME)
    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    hndlr = logging.StreamHandler()
    fmt = NLFormatter(
            fmt="ts=%(asctime)s level=%(levelname)s event=%(msg)s")
    hndlr.setFormatter(fmt)
    log.addHandler(hndlr)
    return log

if __name__ == "__main__":
    main()
