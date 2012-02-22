"""
Main Periscope Application
"""
import asyncmongo
import pymongo
import tornado.web
import tornado.ioloop
from tornado.options import options

# before this import 'periscope' path name is NOT as defined!
import settings
from periscope.handlers import NetworkResourceHandler

class PeriscopeApplication(tornado.web.Application):
    """Defines Periscope Application."""
    def __init__(self):
        self._async_db = None
        self._sync_db = None
        handlers = [
                ("/nodes$", NetworkResourceHandler, dict(collection_name="nodes", base_url="http://localhost:8888/nodes")),
                ("/nodes/(?P<res_id>[^\/]*)$", NetworkResourceHandler, dict(collection_name="nodes", base_url="http://localhost:8888/nodes")),
                (r'/nodes/(?P<res_id>[^\/]+)(?P<kwpath>/.*)?$', NetworkResourceHandler, dict(collection_name="nodes", base_url="http://localhost:8888/nodes")),
                ("/ports$", NetworkResourceHandler, dict(collection_name="ports", base_url="http://localhost:8888/ports")),
                ("/ports/(?P<res_id>[^\/]*)$", NetworkResourceHandler, dict(collection_name="ports", base_url="http://localhost:8888/ports")),
                (r'/ports/(?P<res_id>[^\/]+)(?P<kwpath>/.*)?$', NetworkResourceHandler, dict(collection_name="ports", base_url="http://localhost:8888/ports")),
                
                ("/events$", NetworkResourceHandler, dict(collection_name="events", base_url="http://localhost:8888/events")),
                ("/events/(?P<res_id>[^\/]*)$", NetworkResourceHandler, dict(collection_name="events", base_url="http://localhost:8888/events")),
            ]
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
    app.listen(options.port)
    loop.start()
    logger.info('periscope.end')


if __name__ == "__main__":
    main()
