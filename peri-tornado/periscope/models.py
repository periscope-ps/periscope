#!/usr/bin/env python
"""
Database models.
"""
from json import JSONEncoder
from netlogger import nllog


class MongoEncoder(JSONEncoder):      
    def _iterencode(self, o, markers=None):
        if isinstance(o, ObjectId):
            return """ObjectId("%s")""" % str(o)
        else:
            return JSONEncoder._iterencode(self, o, markers)

class DBLayer(object, nllog.DoesLogging):
    """Thin layer asynchronous model to handle network objects.

    Right now this layer doesn't do much, but provides away to intercept
    the database calls for any future improvements or updates.
    """

    def __init__(self, collection):
        """Intializes with a reference to the mongodb collection."""
        nllog.DoesLogging.__init__(self)
        self._collection = collection

    @property
    def collection(self):
        """Returns a reference to the default mongodb collection."""
        return self._collection

    def find(self, query, callback=None, **kwargs):
        """Finds one or more elements in the collection."""
        self.log.info("find")
        return self.collection.find(query, callback=callback, **kwargs)

    def insert(self, data, callback=None, **kwargs):
        """Inserts data to the collection."""
        self.log.info("insert")
        return self.collection.insert(data, callback=callback, **kwargs)

    def update(self, query, data, callback=None, **kwargs):
        """Updates data found by query in the collection."""
        self.log.info("update")
        return self.collection.update(query, data, callback=callback, **kwargs)

    def remove(self, query, callback=None, **kwargs):
        """Remove objects from the database that matches a query."""
        self.log.info("remove")
        return self.collection.remove(query, callback=callback, **kwargs)
