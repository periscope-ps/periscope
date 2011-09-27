#!/usr/bin/env python

# TODO (AH): MARK FOR REMOVAL

"""
Collected the perfSONAR gLSes root hints from a URL or a file
"""

import logging
import httplib
from urlparse import urlparse

from django.conf import settings

from periscope.measurements.lib.CollectLib import create_psservice


logger = logging.getLogger('periscope')


def get_glss_list():
    """Reads the hints from settings.GLS_ROOT_HINTS and return a string
    list of gLSes.
    """
    parsed = urlparse(settings.GLS_ROOT_HINTS)
    glses = None
    
    if parsed.scheme == 'file':
        f = open(settings.GLS_ROOT_HINTS.replace('file://', ''))
        glses = f.read()
        f.close()
    elif parsed.scheme == 'http':
        conn = httplib.HTTPConnection(parsed.hostname, parsed.port)
        conn.request("GET", parsed.path)
        res = conn.getresponse()
        if res.status != httplib.OK:
            raise Exception("Couldn't connect to gLSes root hints server at '%s'" % settings.GLS_ROOT_HINTS)
        
        glses = res.read()
        conn.close()
    
    if glses is None:
        raise Exception("Cannot read the gLS hints")
    
    # Converts string to array 
    return glses.split()


def populate_roots():
    """Save the list of gLS roots to the topology database
    """
    glses = get_glss_list()
    discoveryEvent = 'http://ogf.org/ns/nmwg/tools/org/perfsonar/service/lookup/discovery/summary/2.0'
    for gls in glses:
        create_psservice(gls, gls, 'gLS', 'Root Hint', [discoveryEvent])

