"""
General Perisocpe Settings.
"""
import logging
import os
import sys
from netlogger import nllog
from tornado.options import define


######################################################################
# Setting up path names.
######################################################################
PERISCOPE_ROOT = os.path.dirname(os.path.abspath(__file__)) + os.sep
sys.path.append(os.path.dirname(os.path.dirname(PERISCOPE_ROOT)))

######################################################################
# Tornado settings.
######################################################################

# default port
define("port", default=8888, help="run on the given port", type=int)

######################################################################
# Periscope Application settings.
######################################################################

# Enable application wide debugging options
DEBUG = True

APP_SETTINGS = {
    'cookie_secret': "43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    'template_path': os.path.join(os.path.dirname(__file__), "templates/"),
    'static_path': os.path.join(os.path.dirname(__file__), "static/"),
    #'static_handler_class': NonCacheStaticFileHandler,
    'xsrf_cookies': False,
    'autoescape': "xhtml_escape",
    'debug': DEBUG,
}


######################################################################
# Mongo Database settings
######################################################################
DB_NAME = "periscope_db"
DB_HOST = "127.0.0.1"
DB_PORT = 27017

# Asyncmongo specific connection configurations
ASYNC_DB = {
    'pool_id': DB_HOST + "_pool",
    'host': DB_HOST,
    'port': DB_PORT,
    'mincached': 1,
    'maxcached': 10,
    'maxconnections': 50,
    'dbname': DB_NAME,
}

# Pymonog specific connection configurations
SYNC_DB = {
    'host': DB_HOST,
    'port': DB_PORT,
}



######################################################################
# Netlogger settings
# (AH): This need to be refactored to more flexible settings
######################################################################
NETLOGGER_NAMESPACE = "periscope"


def config_logger():
    """Configures netlogger"""
    nllog.PROJECT_NAMESPACE = NETLOGGER_NAMESPACE
    #logging.setLoggerClass(nllog.PrettyBPLogger)
    logging.setLoggerClass(nllog.BPLogger)
    log = logging.getLogger(nllog.PROJECT_NAMESPACE)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)
    # set level
    if DEBUG:
        log_level = (logging.WARN, logging.INFO, logging.DEBUG,
                 nllog.TRACE)[3]
    else:
        log_level = (logging.WARN, logging.INFO, logging.DEBUG,
                 nllog.TRACE)[0]
    log.setLevel(log_level)


def get_logger(namespace=NETLOGGER_NAMESPACE):
    """Return logger object"""
    # Test if netlloger is initialized
    if nllog.PROJECT_NAMESPACE != NETLOGGER_NAMESPACE:
        config_logger()
    return nllog.get_logger(namespace)
