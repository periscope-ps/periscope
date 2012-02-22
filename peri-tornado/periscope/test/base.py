"""
Basic classes for unit testing.
"""
import asyncmongo
import pymongo
import random
import tornado.web
from tornado.testing import AsyncTestCase
from tornado.testing import AsyncHTTPTestCase
from periscope.test import settings


class PeriscopeTestCase(AsyncTestCase):
    """Base for Periscope's unit testing test cases.

    This base class sets up two database connections (sync, and async).
    """
    def __init__(self, *args, **kwargs):
        """Initializes internal variables."""
        super(PeriscopeTestCase, self).__init__(*args, **kwargs)
        self._async_db = None
        self._sync_db = None

    @property
    def async_db(self):
        """Returns a reference to asyncmongo DB connection."""
        if not getattr(self, '_async_db', None):
            if hasattr(self, 'io_loop'):
                # Unit testint is going to create different IOLoop instances
                # for each test case, thus we need to make sure that different 
                # connection pools is used
                settings.ASYNC_DB['io_loop'] = self.io_loop
                settings.ASYNC_DB['pool_id'] = "pool_" \
                            "%d" % int(random.random() * 100000)
            self._async_db = asyncmongo.Client(**settings.ASYNC_DB)
        return self._async_db

    @property
    def sync_db(self):
        """Returns a reference to pymongo DB connection."""
        if not getattr(self, '_sync_db', None):
            conn = pymongo.Connection(**settings.SYNC_DB)
            self._sync_db = conn[settings.DB_NAME]
        return self._sync_db


class PeriscopeHTTPTestCase(PeriscopeTestCase, AsyncHTTPTestCase):
    """Base for Periscope's HTTP based unit testing test cases.

    This base class defines tornado.web.Application and sets up
    two database connections (sync, and async).
    """
    def get_app(self):
        class DummyHandler(tornado.web.RequestHandler):
            def get(self):
                self.write("Dummy Handler")
        
        return tornado.web.Application([('/', DummyHandler)])
        
        
    def __init__(self, *args, **kwargs):
        """Initializes internal variables."""
        super(PeriscopeHTTPTestCase, self).__init__(*args, **kwargs)
