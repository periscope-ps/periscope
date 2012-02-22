import functools
from periscope.models import DBLayer
from periscope.test.base import PeriscopeTestCase


class DBLayerTest(PeriscopeTestCase):

    def __init__(self, *args, **kwargs):
        super(DBLayerTest, self).__init__(*args, **kwargs)
        self.collection_name = "test_collection"

    def setUp(self):
        super(DBLayerTest, self).setUp()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)
        self.sync_db.create_collection(self.collection_name)

    def tearDown(self):
        super(DBLayerTest, self).tearDown()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)

    def test_insert(self):
        def handle_insert(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        model = DBLayer(self.async_db[self.collection_name])
        self.assertEqual(model.collection.full_collection_name,
                    self.async_db[self.collection_name].full_collection_name)
        model.insert(data={"two": 2},  callback=handle_insert)
        self.wait()

    def test_delete(self):
        def handle_delete(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        self.sync_db[self.collection_name].insert({"two": 2})
        model = DBLayer(self.async_db[self.collection_name])
        model.remove({"two": 2},  callback=handle_delete)
        self.wait()

    def test_find(self):
        def handle_find(expected, response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response, expected)
            self.stop()

        # Insert some test data directly to the collection
        self.sync_db[self.collection_name].insert({"num": 1})
        self.sync_db[self.collection_name].insert({"num": 2})
        self.sync_db[self.collection_name].insert({"num": 3})
        expected = [{u"num": 2}, {u"num": 3}]
        find_callback = functools.partial(handle_find, expected)

        model = DBLayer(self.async_db[self.collection_name])
        model.find({"num": {"$gte": 2}},
                    callback=find_callback, fields={'_id': 0})
        self.wait()

    def test_update(self):
        def handle_update(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        self.sync_db[self.collection_name].insert({"num": 1})
        model = DBLayer(self.async_db[self.collection_name])
        model.update({"num": 1}, {"num": 2}, callback=handle_update)
        self.wait()

    def test_remove(self):
        def handle_remove(response, error=None):
            self.assertIsNone(error)
            self.assertEqual(response[0]['ok'], 1.0)
            self.stop()

        self.sync_db[self.collection_name].insert({"num": 1})
        model = DBLayer(self.async_db[self.collection_name])
        model.remove({"num": 1}, callback=handle_remove)
        self.wait()
