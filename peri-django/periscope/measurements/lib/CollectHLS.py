#!/usr/bin/env python

# TODO (AH): MARK FOR REMOVAL

"""
Collected the perfSONAR hLSes from a gLS instance
"""

import Queue
import threading
import logging

from psapi.client import ServiceClient
from psapi.query import XQuery
from psapi.protocol import events as psevents

from periscope.topology.models import Service
from periscope.measurements.lib.CollectLib import create_psservice
from periscope.measurements.lib.CollectLib  import get_service_accesspoint

logger = logging.getLogger('periscope')

def look_for_hlses(gls):
    query_text = """
        declare namespace nmwg="http://ggf.org/ns/nmwg/base/2.0/";
        declare namespace perfsonar="http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/";
        declare namespace psservice="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/";
        declare namespace summary="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/summarization/2.0/";
        
        for $metadata in /nmwg:store[@type="LSStore"]/nmwg:metadata
            let $metadata_id := $metadata/@id 
            let $data := /nmwg:store[@type="LSStore"]/nmwg:data[@metadataIdRef=$metadata_id]
            return
                element {"nmwg:metadata"} {
                    attribute id {$metadata_id},
                    element {"perfsonar:subject"} {    
                        $metadata/perfsonar:subject/psservice:service        
                    },
                    $data/nmwg:metadata/nmwg:eventType
                }
    """

    xquery = XQuery(query_text)
    client = ServiceClient(gls)
    logger.info("Send query to gLS: '%s'" % gls) 
    response = client.query(xquery)
    logger.info("Received result from gLS: '%s'" % gls) 
    return response


class HLSCollector(object):
    
    def __init__(self):
        self.lock = threading.RLock()
        
    def populate_hlses(self, gLSService):
        gls = get_service_accesspoint(gLSService)
        
        logger.info("Populating hLSes from gLS: '%s'" % gls) 
        result = look_for_hlses(gls)
        hlses = []
        for meta in result.data:
            service = meta.subject.contents
            if meta.event_types is None:
                events = []
            elif isinstance(meta.event_types, str):
                events = [meta.event_types]
            else: 
                events = list(set(meta.event_types))
                
            # hLSes are also able to handle discovery events
            events.append(psevents.SUMMARY)
            hlses.append({'service':service, 'events':events})
                
        if len(hlses) == 0:
            raise Exception("No hLSes is found at %s" % gls)
        
        for h in hlses:
            try:
                serviceName = h['service'].serviceName
                accessPoint = h['service'].accessPoint
                serviceDescription = h['service'].serviceDescription
                
                service = create_psservice(serviceName, accessPoint, 'hLS', serviceDescription, h['events'])
                
            except Exception, ex:
                logger.error("Found error in '%s': %s" % (serviceName, ex))
                

class ThreadHLSCollect(threading.Thread):
    def __init__(self, glsQueue, collector):
        threading.Thread.__init__(self)
        self.glsQueue = glsQueue
        self.collector = collector
    
    def run(self):
        while True:
            #grabs host from queue
            gls = self.glsQueue.get()
            try:
                print "Collecting from %s" % gls
                self.collector.populate_hlses(gls)
            except Exception, ex:
                # if the gls is not working delete it!
                logger.warning("DELETE gLS: Cannot populate hlses from '%s' because '%s'" % (gls, ex))
                gls.delete()
            #signals to queue job is done
            self.glsQueue.task_done()

gls_queue = Queue.Queue()

def collect_all_hlses():
    """A threaded version that collects all information about hlses from
    the root gls servers.
    """
    services = Service.objects.filter(properties_bag__psserviceproperties__serviceType='gLS')
    for s in services:
        gls_queue.put(s)
    
    collector = HLSCollector()
    for i in range(5):
        t = ThreadHLSCollect(gls_queue, collector)
        t.setDaemon(True)
        t.start()
    
    #gls_queue.join()
