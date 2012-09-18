"""
Main Periscope Application
"""
import asyncmongo
import pymongo
import tornado.web
import tornado.ioloop
from tornado.options import define
from tornado.options import options

# before this import 'periscope' path name is NOT as defined!
import settings
from periscope.handlers import NetworkResourceHandler
from periscope.handlers import CollectionHandler
from periscope.handlers import MainHandler
from periscope.handlers import MIME
from periscope.handlers import SCHEMAS
from periscope.db import DBLayer
from periscope.utils import load_class

# default port
define("port", default=8888, help="run on the given port", type=int)
define("address", default="0.0.0.0", help="default binding IP address", type=str)


class PeriscopeApplication(tornado.web.Application):
    """Defines Periscope Application."""
    
    def get_db_layer(self, collection_name, id_field_name,
            timestamp_field_name, is_capped_collection, capped_collection_size):
        """
        Creates DBLayer instance.
        """
        if collection_name == None:
            return None
        
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
    
    def make_resource_handler(self, name,
                    pattern,
                    base_url,
                    handler_class,
                    model_class,
                    collection_name,
                    schema,
                    is_capped_collection,
                    capped_collection_size,
                    id_field_name,
                    timestamp_field_name,
                    allow_get,
                    allow_post,
                    allow_put,
                    allow_delete,
                    accepted_mime,
                    content_types_mime,
                    **kwargs):
        """
        Creates HTTP Request handler.
        
        Parameters:
        
        name: the name of the URL handler to be used with reverse_url.
        
        pattern: For example "/ports$" or "/ports/(?P<res_id>[^\/]*)$".
            The final URL of the resource is `base_url` + `pattern`.
        
        base_url: see pattern
        
        handler_class: The class handling this request.
            Must inherit `tornado.web.RequestHanlder`
        
        model_class: Database model class for this resource (if any).
        
        collection_name: The name of the database collection storing this resource.
        
        schema: Schemas fot this resource in the form: "{MIME_TYPE: SCHEMA}"
        
        is_capped_collection: If true the database collection is capped.
        
        capped_collection_size: The size of the capped collection (if applicable)
        
        id_field_name: name of the identifier field
        
        timestamp_field_name: name of the timestampe field
        
        allow_get: allow HTTP GET (True or False)
        
        allow_post: allow HTTP POST (True or False)
        
        allow_put: allow HTTP PUT (True or False)
        
        allow_delete: allow HTTP DELETE (True or False)
        
        accepted_mime: list of accepted MIME types
        
        content_types_mime: List of Content types that can be returned to the user
        
        kwargs: additional handler specific arguments
        """
        # Load classes
        if type(handler_class) in [str, unicode]:
            handler_class = load_class(handler_class)
        if type(model_class) in [str, unicode]:
            model_class = load_class(model_class)
        
        # Prepare the DBlayer
        # Prepare the DBlayer
        db_layer = self.get_db_layer(collection_name,
                        id_field_name, timestamp_field_name,
                        is_capped_collection, capped_collection_size)
        
        # Make the handler
        handler = (
            tornado.web.URLSpec(base_url + pattern, handler_class,
                dict(
                    dblayer=db_layer,
                    Id=id_field_name, timestamp=timestamp_field_name,
                    base_url=base_url+pattern,
                    allow_delete=allow_delete,
                    schemas_single=schema,
                    model_class=model_class,
                    **kwargs
                ),
                name=name
            )
        )
        return handler

    def _make_main_handler(self, name,  pattern, base_url, handler_class, resources):
        if type(handler_class) in [str, unicode]:
            handler_class = load_class(handler_class)
        main_handler = (
            tornado.web.URLSpec(base_url + pattern, handler_class,
                dict(
                    resources=resources,
                    base_url=base_url+pattern,
                ),
                name=name
            )
        )
        return main_handler
        
    def __init__(self):
        self._async_db = None
        self._sync_db = None
        handlers = []
        
        for res in settings.Resources:
            handlers.append(self.make_resource_handler(**settings.Resources[res]))
        
        handlers.append(self._make_main_handler(**settings.main_handler_settings))
        tornado.web.Application.__init__(self, handlers,
                    default_host="localhost", **settings.APP_SETTINGS)
    
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


def main():
    """Run periscope"""
    logger = settings.get_logger()
    logger.info('periscope.start')
    loop = tornado.ioloop.IOLoop.instance()
    # parse command line options
    tornado.options.parse_command_line()
    app = PeriscopeApplication()
    app.listen(options.port, address=options.address)
    loop.start()
    logger.info('periscope.end')


if __name__ == "__main__":
    main()
