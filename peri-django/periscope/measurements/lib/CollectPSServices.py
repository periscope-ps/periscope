#!/usr/bin/env python

# TODO (AH): MARK FOR REMOVAL

"""
Collected the perfSONAR services from a hLS instance
"""

import Queue
import threading
import logging

from django.contrib.contenttypes.models import ContentType

from psapi.client import ServiceClient
from psapi.query import XQuery
from psapi.protocol import Data
from psapi.protocol import Metadata
from psapi.protocol import NetUtilSubject
from psapi.protocol import PingerSubject
from psapi.protocol import PsService
from psapi.protocol import OWAMPSubject
from psapi.utils.ipaddress import get_address_type

from periscope.topology.models import EventType
from periscope.topology.models import Node
from periscope.topology.models import Port
from periscope.topology.models import Service
from periscope.topology.models import psServiceWatchList


from periscope.measurements.lib.CollectLib import create_endpoint
from periscope.measurements.lib.CollectLib import create_psservice
from periscope.measurements.lib.CollectLib import get_service_accesspoint


logger = logging.getLogger('periscope')


def query_hls(hls):
    query_text = """
        declare namespace nmwg="http://ggf.org/ns/nmwg/base/2.0/";
        declare namespace perfsonar="http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/";
        declare namespace psservice="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/";
        declare namespace summary="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/summarization/2.0/";
        
        for $metadata in /nmwg:store[@type="LSStore"]/nmwg:metadata
            let $metadata_id := $metadata/@id 
            let $data := /nmwg:store[@type="LSStore"]/nmwg:data[@metadataIdRef=$metadata_id]
            return 
                ($metadata, $data)
    """

    xquery = XQuery(query_text)
    client = ServiceClient(hls)
    logger.info("Send query to hLS: '%s'" % hls) 
    response = client.query(xquery)
    logger.info("Received result from hLS: '%s'" % hls) 
    return response


class ServicesCollector(object):
    
    def __init__(self):
        self.lock = threading.RLock()

    def query(self, hLSService):
        """ Sends query to Service of type hLS
            returns XML string response.
        """
        hls_accessPoint = get_service_accesspoint(hLSService)
        result = query_hls(hls_accessPoint)
        return result

    def process_NetUtilSubject(self, service, meta):
        ptype = ContentType.objects.get_for_model(Port)
        interface = meta.subject.contents

        if interface.IfAddress is None:
            node = Node.objects.filter(names__value=interface.hostName)
            if len(node) == 0:
                port = []
            else:
                port = node[0].get_ports().filter(unis_id__endswith="port=%s" % interface.ifName)
        else:
            port = Port.objects.filter(addresses__value=interface.IfAddress)
        
        if len(port) == 0:
            logger.warning("Port %s, %s was not found" % (interface.hostName, interface.ifName))
        else:
            for event in meta.event_types:
                w = psServiceWatchList.objects.get_or_create(service=service, eventType=EventType.objects.get(value=event), objectType=ptype, objectID=port[0].id)
                if w[1] == 1:
                    w[0].watchedObject = port[0]
                    logger.info("Adding an SNMP MA to port '%s'" % port[0].unis_id)
                    w[0].save()

    def process_EndpointpairSubject(self, service, meta):
        etype = ContentType.objects.get_for_model(Port)
        endpointpair = meta.subject.contents
        try:
            endpoint = create_endpoint(endpointpair.src, \
                                       get_address_type(endpointpair.src), \
                                       endpointpair.dst,
                                       get_address_type(endpointpair.dst))
            if isinstance(meta.event_types, str):
                event_types = [meta.event_types]
            else:
                event_types = meta.event_types
            for event in event_types:
                w = psServiceWatchList.objects.get_or_create(service=service, eventType=EventType.objects.get(value=event), objectType=etype, objectID=endpoint.id)
                if w[1] == 1:
                    w[0].watchedObject = endpoint
                    w[0].save()
        except Exception, ex:
            logger.error("Couldn't add endpoint '%s', from service '%s'" % (ex, get_service_accesspoint(service)))

    def process_result(self, result):
        meta = {}
        data = {}

        # Organize data and metadata in different dicts 
        for tmp in result.data:
            if isinstance(tmp, Metadata):
                meta[tmp.object_id] = tmp
            elif isinstance(tmp, Data):
                if tmp.ref_id in data:
                    data[tmp.ref_id].append(tmp)
                else:
                    data[tmp.ref_id] = [tmp]

        for key, m in meta.iteritems():
            if key not in data:
                data[key] = None
                datums = []
                continue
            datums = data[key]
            event_types = []
            for d in datums: 
                if d.data.event_types is not None:
                    if isinstance(d.data.event_types, list): 
                        for event in d.data.event_types:
                            event_types.append(event)
                    else:
                        event_types.append(d.data.event_types) 

            # to remove duplicates
            event_types = list(set(event_types))
            logger.info('event types: %s' % event_types)
            if isinstance(m.subject.contents, PsService):
                s = m.subject.contents
                service = create_psservice(s.serviceName, s.accessPoint, s.serviceType, s.serviceDescription, event_types)
            
            for d in datums:
                if isinstance(d.data, Metadata):
                    if isinstance(d.data.subject, NetUtilSubject):
                        self.process_NetUtilSubject(service, d.data)
                    elif isinstance(d.data.subject, PingerSubject) or isinstance(d.data.subject, OWAMPSubject):
                        self.process_EndpointpairSubject(service, d.data)
                    else:
                        logger.error("Undefined data type '%s' at service '%s'" % (type(d.data.subject), get_service_accesspoint(service)))
                else:
                    logger.error("Undefined data type '%s' at service '%s'" % (type(d.data), get_service_accesspoint(service)))

    def populate_psservices(self, hLSService):
        result = self.query(hLSService)
        self.process_result(result)


class ThreadServicesCollect(threading.Thread):
    def __init__(self, hlsQueue, collector):
        threading.Thread.__init__(self)
        self.hlsQueue = hlsQueue
        self.collector = collector

    def run(self):
        while True:
            #grabs host from queue
            hls = self.hlsQueue.get()
            try:
                print "Collecting from %s" % hls
                self.collector.populate_psservices(hls)
            except Exception, ex:
                # if the gls is not working delete it!'h
                logger.warning("Delete hLS: Cannot populate services because '%s'" % ex)
                hls.delete()
            #signals to queue job is done
            self.hlsQueue.task_done()

hls_queue = Queue.Queue()

def collect_all_services():
    """A threaded version that collects all information about hlses from
    the root gls servers.
    """
    services = Service.objects.filter(properties_bag__psserviceproperties__serviceType='hLS')
    for s in services:
        hls_queue.put(s)

    collector = ServicesCollector()
    for i in range(25):
        t = ThreadServicesCollect(hls_queue, collector)
        t.setDaemon(True)
        t.start()

    #hls_queue.join()
