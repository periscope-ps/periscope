######################################################################
# Mongo Database settings for unit testing
######################################################################
DB_NAME = "periscope_test"
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


NETLOGGER_NAMESPACE = "periscope"
import logging
from netlogger import nllog
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
    
    log_level = (logging.WARN, logging.INFO, logging.DEBUG,
             nllog.TRACE)[3]
    
    log.setLevel(10)


def get_logger(namespace=NETLOGGER_NAMESPACE):
    """Return logger object"""
    # Test if netlloger is initialized
    if nllog.PROJECT_NAMESPACE != NETLOGGER_NAMESPACE:
        config_logger()
    return nllog.get_logger(namespace)

config_logger()
