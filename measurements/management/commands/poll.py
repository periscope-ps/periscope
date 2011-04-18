#!/usr/bin/env python

# Adpated from GENI branch, should merge into more generic poll command


import logging
import time
import random
from datetime import datetime

from lxml import etree
from urlparse import urlparse

from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


from periscope.measurements.models import Metadata, Data
from periscope.topology.lib.util import create_urn, get_urn_value


from periscope.topology.models import CloudNodeProperties
from periscope.topology.models import EventType
from periscope.topology.models import EndPointPair
from periscope.topology.models import NetworkObjectNames
from periscope.topology.models import Node
from periscope.topology.models import NodeAddresses
from periscope.topology.models import Service
from periscope.topology.models import PS_NAMESPACE as PSSERVICE_NS
from periscope.topology.models import Path
from periscope.topology.models import Port
from periscope.topology.models import psServiceProperties
from periscope.topology.models import psServiceWatchList

from periscope.topology.models import NMWG_NAMESPACE as NMWG

from periscope.measurements.lib.util import parse_snmp_response
from periscope.measurements.lib.util import parse_snmp_response_data
from periscope.measurements.lib.CollectLib import get_service_accesspoint
from periscope.measurements.lib.CollectLib import query_psservice

NMWGT = 'http://ggf.org/ns/nmwg/topology/2.0/'

logger = logging.getLogger('periscope')


# TODO: create endppoints measurements
def create_measurement_mds():
    # Create metadata only for ports that are part of a path
    snmp = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/utilization/2.0')
    sent_result = EventType.objects.get_or_create(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0')
    sent = sent_result[0]
    recv_result = EventType.objects.get_or_create(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0')
    recv = recv_result[0]
    if sent_result[1] == True:
        sent.save()
    
    if recv_result[1] == True:
        recv.save()
    
    port_type= ContentType.objects.get_for_model(Port)
    for path in Path.objects.all():
        for hop in path.hops.all():
            link = hop.target.toRealType()
            sport = link.get_source()
            dport = link.get_sink()
            
            service = psServiceWatchList.objects.filter(objectType=port_type, objectID=sport.id, eventType=snmp)
            if len(service) > 0:
                result = Metadata.objects.get_or_create(objectType=port_type, objectID=sport.id, event_type=sent, poll=True)
                if result[1] == True:
                    result[0].service = service[0].service
                    result[0].save()
                result = Metadata.objects.get_or_create(objectType=port_type, objectID=sport.id, event_type=recv, poll=True)
                if result[1] == True:
                    result[0].service = service[0].service
                    result[0].save()
            
            service = psServiceWatchList.objects.filter(objectType=port_type, objectID=dport.id, eventType=snmp)
            if len(service) > 0:
                result = Metadata.objects.get_or_create(objectType=port_type, objectID=dport.id, event_type=sent, poll=True)
                if result[1] == True:
                    result[0].service = service[0].service
                    result[0].save()
                result = Metadata.objects.get_or_create(objectType=port_type, objectID=dport.id, event_type=recv, poll=True)
                if result[1] == True:
                    result[0].service = service[0].service
                    result[0].save()


def make_snmp_request(port, start_time, end_time):
    
    if len(port.addresses.filter(type='ipv4')) > 0:
        address = port.addresses.filter(type='ipv4')[0]
        ifname = None
    else:
        address = None
        ifname = get_urn_value(port.unis_id, 'port')
    
    hostname = get_urn_value(port.unis_id, 'node')
     
    msg_address = """
    
    
  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadataMETAID">
    <netutil:subject xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
                     id="s-in-netutil-METAID">
      <nmwgt:interface xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/">
        <nmwgt:ifAddress>%s</nmwgt:ifAddress>
      </nmwgt:interface>
    </netutil:subject>
    <nmwg:eventType>http://ggf.org/ns/nmwg/characteristic/utilization/2.0</nmwg:eventType>
  </nmwg:metadata>

  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadataMETAIDc"> 
    <select:subject xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/"
                    id="subjectMETAIDc" metadataIdRef="metadataMETAID" /> 
    <select:parameters id="param2c" xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/">      
      <nmwg:parameter name="startTime">%s</nmwg:parameter> 
      <nmwg:parameter name="endTime">%s</nmwg:parameter>
      
      
    </select:parameters> 
    <nmwg:eventType>http://ggf.org/ns/nmwg/ops/select/2.0</nmwg:eventType> 
  </nmwg:metadata> 
  
  <nmwg:data xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
             id="dataMETAID" metadataIdRef="metadataMETAIDc"/>
""" 
    
    msg_ifname = """
  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadataMETAID">
    <netutil:subject xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
                     id="s-in-netutil-METAID">
      <nmwgt:interface xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/">
        <nmwgt:hostName>%s</nmwgt:hostName>
        <nmwgt:ifName>%s</nmwgt:ifName>
      </nmwgt:interface>
    </netutil:subject>
    <nmwg:eventType>http://ggf.org/ns/nmwg/characteristic/utilization/2.0</nmwg:eventType>
  </nmwg:metadata>

  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadataMETAIDc"> 
    <select:subject xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/"
                    id="subjectMETAIDc" metadataIdRef="metadataMETAID" /> 
    <select:parameters id="param2c" xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/">      
      <nmwg:parameter name="startTime">%s</nmwg:parameter> 
      <nmwg:parameter name="endTime">%s</nmwg:parameter>
      
      
    </select:parameters> 
    <nmwg:eventType>http://ggf.org/ns/nmwg/ops/select/2.0</nmwg:eventType> 
  </nmwg:metadata> 
  
  <nmwg:data xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
             id="dataMETAID" metadataIdRef="metadataMETAIDc"/>
"""
    if address is None:
        msg = msg_ifname % (hostname, ifname, start_time, end_time)
    else:
        msg = msg_address % (address, start_time, end_time)
        
    metaid = random.randint(1, 1000000)
    msg = msg.replace('METAID', metaid.__str__())
    return {'metaid': "metadata%ic" % metaid, 'xml':msg}


def save_data(meta, data):
    for v in data:
        result = Data(metadata=meta, time=v['timeValue'], value=v['value'], units=v['valueUnits'])
        result.save()


def poll_snmp_data(start_time, end_time):
    sent = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0')
    recv = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0')
            
    metadata = Metadata.objects.filter(poll=True, event_type=sent)
    metadata_recv = Metadata.objects.filter(poll=True, event_type=recv)
    services = {}
    for m in metadata:
        if m.service not in services:
            services[m.service] = {'meta': {}}
        services[m.service]['meta'][m] = None
        
    for service in services:
        services[service]['request'] = ''
        for m in services[service]['meta']:
            result = make_snmp_request(m.subject, start_time, end_time)
            services[service]['meta'][m] = result['metaid']
            services[service]['request'] += result['xml']
            
        services[service]['request'] = """
<nmwg:message xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
              xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
              xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
              xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/"
              type="SetupDataRequest" id="SetupDataRequest1">
              """ + services[service]['request'] + "\n</nmwg:message>"
        
    for service in services:
        sss = time.time()
        response = query_psservice(service, services[service]['request'])
        eee = time.time()
        print "query time: %f" % (eee - sss)
        root = etree.fromstring(response)
        for m in services[service]['meta']:
            metas = root.findall(".//{%s}metadata[@metadataIdRef=\"%s\"]" % (NMWG, services[service]['meta'][m]))
            if metas == None:
                continue
            direction = metas[0].find(".//{%s}direction" % (NMWGT))
            
            if direction.text == 'out':
                meta_out = metas[0]
                meta_in = metas[1]
            else:
                meta_out = metas[1]
                meta_in = metas[0]
            
            meta_in_id = meta_in.attrib['id']
            meta_out_id = meta_out.attrib['id']
            
            data_in = root.find(".//{%s}data[@metadataIdRef=\"%s\"]" % (NMWG, meta_in_id))
            data_out = root.find(".//{%s}data[@metadataIdRef=\"%s\"]" % (NMWG, meta_out_id))
            
            parsed_in = parse_snmp_response_data(data_in)
            parsed_out = parse_snmp_response_data(data_out)
            save_data(m, parsed_out)
            recv_meta = metadata_recv.get(objectID=m.subject.id)
            save_data(recv_meta, parsed_in)


def query_metakey(service, src, dst):
    msg = """
<nmwg:message type="MetadataKeyRequest" id="metadataKeyRequest1"
              xmlns:iperf= "http://ggf.org/ns/nmwg/tools/iperf/2.0/"
              xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
              xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/"
              xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
              xmlns:nmtm="http://ggf.org/ns/nmwg/time/2.0/"> 
  <nmwg:metadata id="meta1" xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"> 
    <iperf:subject xmlns:iperf= "http://ggf.org/ns/nmwg/tools/iperf/2.0/" id="s-in-iperf-1"> 
      <nmwgt:endPointPair xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"> 
        <nmwgt:src value="%s" /> 
        <nmwgt:dst value="%s" /> 
      </nmwgt:endPointPair> 
    </iperf:subject> 
    <nmwg:eventType>http://ggf.org/ns/nmwg/tools/iperf/2.0</nmwg:eventType> 
    <nmwg:parameters id="parameters-0">
        <nmwg:parameter name="protocol">TCP</nmwg:parameter>
    </nmwg:parameters>
  </nmwg:metadata> 
  <nmwg:data id="data1" metadataIdRef="meta1" xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"/> 
  </nmwg:message>
"""
    
    result = query_psservice(service, msg % (src, dst))
    root = etree.fromstring(result)
    meta = root.find(".//{%s}parameter[@name=\"maKey\"]" % NMWG)
    if meta == None:
        return None
    else:
        return meta.text


def get_endpoint_metakey(service, endpoint):
    src = endpoint.src.toRealType()
    dst = endpoint.dst.toRealType()
    for s in src.addresses.all():
        for d in dst.addresses.all():
            meta = query_metakey(service, s.value, d.value)
            if meta is not None:
                return meta
    return None


def create_measurement_mds_iperf():
    iperf = EventType.objects.get(value='http://ggf.org/ns/nmwg/tools/iperf/2.0')
    cloud_nodes = Node.objects.filter(type='cloud')
    ports = []
    for node in cloud_nodes:
        props = CloudNodeProperties.objects.get(parent=node)
        for port in props.bwctl.all():
            ports.append(port)
    
    wiperf = psServiceWatchList.objects.filter(eventType=iperf)
    etype= ContentType.objects.get_for_model(EndPointPair)
    for src in ports:
        for dst in ports:
            if src == dst:
                continue
            ends = EndPointPair.objects.filter(src__unis_id=src.unis_id, dst__unis_id=dst.unis_id)
            for end in ends:
                watches = wiperf.filter(objectID=end.id, objectType=etype)
                for w in watches:
                    result = Metadata.objects.get_or_create(objectType=etype, objectID=end.id, event_type=iperf, poll=True)
                    if result[1] == True:
                        result[0].service = service[0].service
                        result[0].save()


class Command(BaseCommand):
    help = "Finds and polls perfSONAR MAs for measurement data.\n"
    
    def handle(self, *args, **options):
        window =  60
        
        if Metadata.objects.count() == 0:
            if create_measurement_mds() == None:
                return
                
        now = int(time.time())
        poll_snmp_data(now - window, now)
            
