import socket
HOSTNAME = socket.gethostname() # this needs to get the fqdn for DOMAIN to be right down below
#                                 works for geni nodes, but may not for everything.

# Scheduler Stuff
PROBES=["cpu", "net", "mem"]
CHECK_INTERVAL=3 # number of seconds between checking the
#                  settings files to see if anything changed
SLEEP_FACTOR=1

# Probe stuff
UNIS_URL="http://dev.incntre.iu.edu"
#UNIS_URL="http://127.0.0.1:8888"
COLLECTION_INTERVAL=1
REPORTING_INTERVAL=10
COLLECTION_TIME=0 # total time to continue collecting, 0 means forever
SUBJECT="%s/nodes/%s" % (UNIS_URL, HOSTNAME)
METADATA_CACHE="~/.blippmd"
PROC_DIR="/proc"
COLLECTION_SIZE=20000000 # ~20 megabytes
COLLECTION_TTL=1500000 # ~17 days
MS_URL=""
# MS_URL="http://127.0.0.1:8855"
GEMINI_NODE_INFO="/usr/local/etc/node.info"

# UNIS settings
try:
    DOMAIN = HOSTNAME.split('.', 1)[1]
except Exception:
    DOMAIN = HOSTNAME
URN_STRING = "urn:ogf:network:domain=" + DOMAIN + ":"
LOCATION = {"location":{"institution": "GENI"}}

# Static stuff
SCHEMAS = {
    'networkresource': 'http://unis.incntre.iu.edu/schema/20120709/networkresource#',
    'node': 'http://unis.incntre.iu.edu/schema/20120709/node#',
    'domain': 'http://unis.incntre.iu.edu/schema/20120709/domain#',
    'port': 'http://unis.incntre.iu.edu/schema/20120709/port#',
    'link': 'http://unis.incntre.iu.edu/schema/20120709/link#',
    'path': 'http://unis.incntre.iu.edu/schema/20120709/path#',
    'network': 'http://unis.incntre.iu.edu/schema/20120709/network#',
    'topology': 'http://unis.incntre.iu.edu/schema/20120709/topology#',
    'service': 'http://unis.incntre.iu.edu/schema/20120709/service#',
    'blipp': 'http://unis.incntre.iu.edu/schema/20120709/blipp#',
    'metadata': 'http://unis.incntre.iu.edu/schema/20120709/metadata#',
    'datum': 'http://unis.incntre.iu.edu/schema/20120709/datum#',
    'data': 'http://unis.incntre.iu.edu/schema/20120709/data#'
}

MIME = {
    'HTML': 'text/html',
    'JSON': 'application/json',
    'PLAIN': 'text/plain',
    'SSE': 'text/event-stream',
    'PSJSON': 'application/perfsonar+json',
    'PSBSON': 'application/perfsonar+bson',
    'PSXML': 'application/perfsonar+xml',
    }



##################################################################
# Netlogger stuff... pasted from Ahmed's peri-tornado
##################################################################
import logging
from netlogger import nllog

DEBUG = True
TRACE = False
NETLOGGER_NAMESPACE = "blipp"

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
    if TRACE:
        log_level = (logging.WARN, logging.INFO, logging.DEBUG,
                 nllog.TRACE)[3]
    elif DEBUG:
        log_level = (logging.WARN, logging.INFO, logging.DEBUG,
                 nllog.TRACE)[2]
    
    else:
        log_level = (logging.WARN, logging.INFO, logging.DEBUG,
                 nllog.TRACE)[0]
    log.setLevel(log_level)


def get_logger(namespace=NETLOGGER_NAMESPACE):
    """Return logger object"""
    # Test if netlogger is initialized
    if nllog.PROJECT_NAMESPACE != NETLOGGER_NAMESPACE:
        config_logger()
    return nllog.get_logger(namespace)
