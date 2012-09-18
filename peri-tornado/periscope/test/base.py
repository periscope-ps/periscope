"""
Basic classes for unit testing.
"""
import asyncmongo
import pymongo
import random
import tornado.web
import unittest2
from tornado.testing import AsyncTestCase
from tornado.testing import AsyncHTTPTestCase
from periscope.test import settings
from periscope.db import DBLayer
from tornado.ioloop import IOLoop


class PeriscopeTestCase(AsyncTestCase, unittest2.TestCase):
    """Base for Periscope's unit testing test cases.

    This base class sets up two database connections (sync, and async).
    """
    def __init__(self, *args, **kwargs):
        """Initializes internal variables."""
        super(PeriscopeTestCase, self).__init__(*args, **kwargs)
        self._async_db = None
        self._sync_db = None

    def get_new_ioloop(self):
        return  IOLoop.instance()
    
    @property
    def async_db(self):
        """Returns a reference to asyncmongo DB connection."""
        if not getattr(self, '_async_db', None):
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
        
        class TestApp(tornado.web.Application):
            
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
        
            def get_db_layer(self, collection_name, id_field_name,
                timestamp_field_name, is_capped_collection, capped_collection_size):
                # Initialize the capped collection, if necessary!
                if is_capped_collection and \
                        collection_name not in self.sync_db.collection_names():
                    self.sync_db.create_collection(collection_name,
                                    capped=True,
                                    size=capped_collection_size)
                # Make indexes
                self.sync_db[collection_name].ensure_index([
                        (id_field_name, 1),
                        (timestamp_field_name, -1)
                    ],
                    unique=True)
                
                # Prepare the DBLayer
                db_layer = DBLayer(self.async_db,
                    collection_name,
                    is_capped_collection,
                    id_field_name,
                    timestamp_field_name
                )
                
                return db_layer
            
        
        return TestApp([('/', DummyHandler)])
        
        
    def __init__(self, *args, **kwargs):
        """Initializes internal variables."""
        super(PeriscopeHTTPTestCase, self).__init__(*args, **kwargs)
