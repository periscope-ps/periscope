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
    # TODO (AH): work on defining all top level resources
    supported_netres = ['nodes', 'ports', 'networks', 'links', 'events']
    
    def _make_handlers(self, resources):
        handlers = []
        for res in resources:
            handlers.append(("/%s$" % res, NetworkResourceHandler, dict(collection_name=res, base_url="/%s" % res)))
            handlers.append(("/%s/(?P<res_id>[^\/]*)$" % res, NetworkResourceHandler, dict(collection_name=res, base_url="/%s" % res)))
        return handlers
            
    def __init__(self):
        self._async_db = None
        self._sync_db = None
        handlers =  self._make_handlers(self.supported_netres)
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
