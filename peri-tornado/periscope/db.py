#!/usr/bin/env python
"""
Databases related classes
"""
import time
from json import JSONEncoder
from netlogger import nllog
from pymongo.objectid import ObjectId


class MongoEncoder(JSONEncoder):
    """Special JSON encoder that converts Mongo ObjectIDs to string"""
    def _iterencode(self, obj, markers=None):
        if isinstance(obj, ObjectId):
            return """ObjectId("%s")""" % str(obj)
        else:
            return JSONEncoder._iterencode(self, obj, markers)


class DBLayer(object, nllog.DoesLogging):
    """Thin layer asynchronous model to handle network objects.

    Right now this layer doesn't do much, but provides away to intercept
    the database calls for any future improvements or updates.

    Unfortuantly uncapped collections in Mongo must have a uniqe '_id'
    field, so this layer will generate one for each insert based on the
    network resource id and the revision number.
    """

    def __init__(self, client, collection_name, capped=False, Id="id", \
        timestamp="ts"):
        """Intializes with a reference to the mongodb collection."""
        nllog.DoesLogging.__init__(self)
        self.Id = Id
        self.timestamp = timestamp
        self.capped = capped
        self._collection_name = collection_name
        self._client = client

    @property
    def collection(self):
        """Returns a reference to the default mongodb collection."""
        return self._client[self._collection_name]

    def find(self, query, callback=None, **kwargs):
        """Finds one or more elements in the collection."""
        self.log.info("find")
        fields = kwargs.pop("fields", {})
        fields["_id"] = 0
        return self.collection.find(query, callback=callback,
                                    fields=fields, **kwargs)

    def _insert_id(self, data):
        if "_id" not in data and not self.capped:
            res_id = data.get(self.Id, str(ObjectId()))
            timestamp = data.get(self.timestamp, int(time.time() * 1000000))
            data["_id"] = "%s:%s" % (res_id, timestamp)
            
    def insert(self, data, callback=None, **kwargs):
        """Inserts data to the collection."""
        self.log.info("insert")
        if isinstance(data, list) and not self.capped:
            for item in data:
                self._insert_id(item)
        elif not self.capped:
            self._insert_id(data)
            
        
        return self.collection.insert(data, callback=callback, **kwargs)

    def update(self, query, data, callback=None, **kwargs):
        """Updates data found by query in the collection."""
        self.log.info("update")
        return self.collection.update(query, data, callback=callback, **kwargs)

    def remove(self, query, callback=None, **kwargs):
        """Remove objects from the database that matches a query."""
        self.log.info("remove")
        return self.collection.remove(query, callback=callback, **kwargs)


