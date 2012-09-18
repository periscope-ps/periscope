#!/usr/bin/env python
"""
Databases related tests
"""

import functools
from periscope.db import DBLayer
from periscope.test.base import PeriscopeTestCase
from mock import Mock
import copy


class DBLayerIntegrationTest(PeriscopeTestCase):

    def __init__(self, *args, **kwargs):
        super(DBLayerIntegrationTest, self).__init__(*args, **kwargs)
        self.collection_name = "test_collection"

    def setUp(self):
        super(DBLayerIntegrationTest, self).setUp()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)
        self.sync_db.create_collection(self.collection_name)

    def tearDown(self):
        super(DBLayerIntegrationTest, self).tearDown()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)

    def test_insert(self):
        def handle_insert(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        model = DBLayer(self.async_db, self.collection_name)
        self.assertEqual(model.collection.full_collection_name,
                    self.async_db[self.collection_name].full_collection_name)
        model.insert(data={"id": "1", "two": 2},  callback=handle_insert)
        self.wait()

    def test_delete(self):
        def handle_delete(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        self.sync_db[self.collection_name].insert({"two": 2})
        model = DBLayer(self.async_db, self.collection_name)
        model.remove({"two": 2},  callback=handle_delete)
        self.wait()

    def test_find(self):
        def handle_find(expected, response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response, expected)
            self.stop()

        # Insert some test data directly to the collection
        self.sync_db[self.collection_name].insert({"_id": "1", "num": 1})
        self.sync_db[self.collection_name].insert({"_id": "2", "num": 2})
        self.sync_db[self.collection_name].insert({"_id": "3", "num": 3})
        expected = [{u"num": 2}, {u"num": 3}]
        find_callback = functools.partial(handle_find, expected)

        model = DBLayer(self.async_db, self.collection_name)
        model.find({"num": {"$gte": 2}},
                    callback=find_callback)
        self.wait()

    def test_update(self):
        def handle_update(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        self.sync_db[self.collection_name].insert({"num": 1})
        model = DBLayer(self.async_db, self.collection_name)
        model.update({"num": 1}, {"num": 2}, callback=handle_update)
        self.wait()

    def test_remove(self):
        def handle_remove(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        self.sync_db[self.collection_name].insert({"num": 1})
        model = DBLayer(self.async_db, self.collection_name)
        model.remove({"num": 1}, callback=handle_remove)
        self.wait()


class DBLayerTest(PeriscopeTestCase):
    def test_insert(self):
        # Arrange
        response = [{u'connectionId': 1, u'ok': 1.0, u'err': None, u'n': 0}]
        collection_name = "collection_insert"
        collection = Mock(name=collection_name)
        collection.insert.return_value = None
        collection.insert.side_effect = lambda *args, **kwargs: kwargs['callback'](response, error=None)
        client = {collection_name: collection}
        callback = Mock(name="insert_callback")
        callback.side_effect = lambda response, error : self.stop()
        ts = 1330921125000000
        data = {"id": "1", "ts": ts, "two": 2}
        expected = copy.copy(data)
        expected['_id'] = "1:"+str(ts)
        # Act
        model = DBLayer(client, collection_name)
        model.insert(data, callback=callback)
        self.wait()
        # Assert
        collection.insert.assert_called_once_with(expected,  callback=callback)
        callback.assert_called_once_with(response,  error=None)
    
    def test_delete(self):
        response = [{u'connectionId': 1, u'ok': 1.0, u'err': None, u'n': 0}]
        query = {"id": "1", "two": 2}
        collection_name = "collection_remove"
        collection = Mock(name=collection_name)
        collection.remove.return_value = None
        collection.remove.side_effect = lambda *args, **kwargs: kwargs['callback'](response, error=None)
        client = {collection_name: collection}
        callback = Mock(name="remove_callback")
        callback.side_effect = lambda response, error : self.stop()
        # Act
        model = DBLayer(client, collection_name)
        model.remove(query, callback=callback)
        self.wait()
        # Assert
        collection.remove.assert_called_once_with(query, callback=callback)
        callback.assert_called_once_with(response, error=None)

    def test_find(self):
        # Arrange
        response = [{"_id": "2", "num": 2}, {"_id": "3", "num": 3}]
        expected = [{"_id": "2", "num": 2}, {"_id": "3", "num": 3}]
        query = {"num": {"$gte": 2},}
        collection_name = "collection_find"
        collection = Mock(name=collection_name)
        collection.find.return_value = None
        collection.find.side_effect = lambda *args, **kwargs: kwargs['callback'](response, error=None)
        client = {collection_name: collection}
        callback = Mock(name="find_callback")
        callback.side_effect = lambda response, error : self.stop()
        # Act
        model = DBLayer(client, collection_name)
        model.find(query, callback=callback)
        self.wait()
        # Assert
        self.assertEqual(collection.find.call_args[0], (query,))
        callback.assert_called_once_with(expected, error=None)
    
    def test_update(self):
        # Arrange
        response = [{u'updatedExisting': True, u'connectionId': 1, u'ok': 1.0, u'err': None, u'n': 1}]
        query = {"id": 1}
        data = {"num": 2}
        collection_name = "collection_update"
        collection = Mock(name=collection_name)
        collection.update.return_value = None
        collection.update.side_effect = lambda *args, **kwargs: kwargs['callback'](response, error=None)
        client = {collection_name: collection}
        callback = Mock(name="update_callback")
        callback.side_effect = lambda response, error : self.stop()
        # Act
        model = DBLayer(client, collection_name)
        model.update(query, data, callback=callback)
        self.wait()
        # Assert
        collection.update.assert_called_once_with({'id': 1}, data, callback=callback)
        callback.assert_called_once_with(response, error=None)
