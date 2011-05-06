import logging
import time

from lxml import etree
from urlparse import urlparse

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from periscope.measurements.models import Metadata, Data
from periscope.topology.lib.util import create_urn, get_urn_value
from periscope.topology.models import Service, PS_NAMESPACE as PSSERVICE_NS,\
    Node, psServiceProperties, EventType, NodeAddresses, Port,\
    NetworkObjectNames

from periscope.measurements.lib.SimpleClient import SimpleClient
from periscope.measurements.lib.util import parse_snmp_response


logger = logging.getLogger('periscope')

def is_psservice_available(service):
    return True

SNMP_MA_XQUERY = '''
declare namespace nmwg="http://ggf.org/ns/nmwg/base/2.0/";
declare namespace perfsonar="http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/";
declare namespace psservice="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/";
for $store in /nmwg:store[@type='LSStore'] return
    if (exists($store/nmwg:metadata)) then
        let $metadata := $store/nmwg:metadata
        let $node_id := $metadata/perfsonar:subject/psservice:service/psservice:serviceNode
        where contains($node_id, '%s:node=') and
              exists( /nmwg:store[@type='LSStore']/nmwg:data[@metadataIdRef=$metadata/@id
                      ]/nmwg:metadata/nmwg:eventType[
                          contains(., 'http://ggf.org/ns/nmwg/characteristic/utilization/2.0')])
        return $metadata/perfsonar:subject/psservice:service
    else ()
'''

PORT_MDK_REQUEST = '''
<nmwg:message xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
    xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
    xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
    type="MetadataKeyRequest" id="metadataKeyRequest1">

    <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/" id="metadata.5">
       <netutil:subject xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/" id="s-util">
         <nmwgt:interface xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/">
         </nmwgt:interface>
       </netutil:subject>
       <nmwg:eventType>http://ggf.org/ns/nmwg/characteristic/utilization/2.0</nmwg:eventType>
    </nmwg:metadata>

    <nmwg:data xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/" id="data1" metadataIdRef="metadata.5"/>
</nmwg:message>
'''

SETUPDATA_REQUEST = """
<nmwg:message xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
              xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
              xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
              type="SetupDataRequest" id="SetupDataRequest1">

  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/" 
                 id="metadata1">
    <nmwg:key id="key1">
      <nmwg:parameters id="params.0">
        <nmwg:parameter name="maKey">%s</nmwg:parameter>
      </nmwg:parameters>
    </nmwg:key>
  </nmwg:metadata> 

  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadata1c">
    <select:subject xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/"
                    id="subject1c" metadataIdRef="metadata1" />
    <select:parameters id="param2c" xmlns:select="http://ggf.org/ns/nmwg/ops/select/2.0/">
      <nmwg:parameter name="startTime">%s</nmwg:parameter>
    </select:parameters>
    <nmwg:eventType>http://ggf.org/ns/nmwg/ops/select/2.0</nmwg:eventType>
  </nmwg:metadata>

  <nmwg:data xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
             id="data1" metadataIdRef="metadata1c"/>

</nmwg:message>
"""

NODE_KEY_MD_XPATH = '''
//*[local-name()='metadata' and
    ./*[local-name()='subject']/*[local-name()='node']/*[
        local-name()='hostName' and contains('%s', normalize-space(text()))] and
    count(./*[local-name()='eventType' and normalize-space(text())='%s']) > 0]/@id
'''

PORT_KEY_MD_XPATH = '''
//*[local-name()='metadata' and
    ./*[local-name()='subject']/*[local-name()='interface' and 
           ./*[local-name()='ifName' and contains('%s', normalize-space(text()))] and
           (string-length('%s') < 1 or ./*[local-name()='direction' and normalize-space(text())='%s'])] and
    count(./*[local-name()='eventType' and normalize-space(text())='%s']) > 0]/@id
'''

KEY_XPATH = '''
//*[local-name()='data' and @metadataIdRef='%s']/*[local-name()='key']/*[
      local-name()='parameters']/*[local-name()='parameter' and @name='maKey']/text()
'''


def query_psservice(service, message):
    try:
        psservice = psServiceProperties.objects.get(parent=service)
    except psServiceProperties.DoesNotExist:
        logger.error("No psServiceProperties for service (" + service.unis_id + ")")
        return None
    
    try:
        url = urlparse(psservice.accessPoint)
        
        client = SimpleClient(host=url.hostname, port=url.port, uri=url.path)
        response = client.send_request(message)
    except:
        logger.error("Error contacting service at " + psservice.accessPoint);
        return None
    
    return response
    

def create_measurement_mds():
    NODE_ETS = ( 
        EventType.objects.get_or_create(
            value="http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0")[0],
        EventType.objects.get_or_create(
            value="http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0")[0],
        EventType.objects.get_or_create(
            value="http://ggf.org/ns/nmwg/characteristic/cpu/utilization/system/2.0")[0],
        EventType.objects.get_or_create(
            value="http://ggf.org/ns/nmwg/characteristic/memory/main/free/2.0")[0],
        )
    
    md = None

    node_type = ContentType.objects.get_for_model(Node)
    for node in Node.objects.all():
        for et in NODE_ETS:
            md = Metadata.objects.get_or_create(objectType=node_type, objectID=node.id, event_type=et, poll=True)
    
    
    PORT_ETS = (
        EventType.objects.get_or_create(
            value="http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0")[0],
        EventType.objects.get_or_create(
            value="http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0")[0],
        )

    port_type = ContentType.objects.get_for_model(Port)    
    for port in Port.objects.all():
        for et in PORT_ETS:
            md = Metadata.objects.get_or_create(objectType=port_type, objectID=port.id, event_type=et, poll=True)

    return md
            
# TODO: Adapted from CollectLib, should eventually merge
@transaction.commit_on_success
def create_psservice(node_id, name, access_point, type, description):
    # Check if the service already exists
    services = Service.objects.filter(properties_bag__psserviceproperties__accessPoint=access_point)
    if len(services) > 0:
        return services[0]
    
    # See if we can find node by id, but not necessary
    node = None
    try:
        node = Node.objects.get(unis_id=node_id)
    except Node.DoesNotExist:
        pass
    
    service = Service.objects.create(parent=node, unis_id=node_id+':service=snmpma')
    
    props = psServiceProperties()
    props.serviceName = name
    props.accessPoint = access_point
    props.serviceType = type
    props.serviceDescription = description
    
    service.properties_bag.add(props)
    service.save()
    
    return service
    
# TODO: Right now we support a single MA, and the eTs
#   are hardcoded to Ganglia's eTs for LAMP.
class Command(BaseCommand):
    help = "Finds and polls perfSONAR MAs for measurement data.\n"
    
    def handle(self, *args, **options):
        window = 24*60*60
        
        if Metadata.objects.count() == 0:
            if create_measurement_mds() == None:
                return
        
        mds = Metadata.objects.filter(poll=True)
        
        # TODO: Assumes all mds use the same service, and single domain
        ma = mds[0].service
        if ma is None or not is_psservice_available(ma):
            # Hardcoded MA for ESCPS
            ma = create_psservice("urn:ogf:network:domain=internet2.edu:node=packrat", "ESCPSMA",
                                  "http://packrat.internet2.edu:2010/perfSONAR_PS/services/snmp/ESCPSMA",
                                  "SNMPMA", "ESCPS SNMP MA")
            Metadata.objects.update(service=ma)

        Metadata.objects.update(key=None)        
        # Update metadata keys if we have any missing
        if mds.filter(key=None).count() > 0:
            node_mds = []
            port_mds = []
            
            for md in mds.filter(key=None):
                if hasattr(md.subject, 'port'):
                    port_mds.append(md)
            
            if len(port_mds):
                response = query_psservice(ma, PORT_MDK_REQUEST)
                root = etree.fromstring(response)
                
                for md in port_mds:
                    names = []
                    for port_names in NetworkObjectNames.objects.filter(networkobject=md.subject):
                        names.append(port_names.name.value)
                    names = '~^~'.join(names)

                    event_type = md.event_type.value 

                    # Special cases
                    direction = ''
                    if md.event_type.value == \
                            'http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0':
                        direction = 'in'
                        event_type = 'http://ggf.org/ns/nmwg/characteristic/utilization/2.0'
                    elif md.event_type.value == \
                            'http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0':
                        direction = 'out'
                        event_type = 'http://ggf.org/ns/nmwg/characteristic/utilization/2.0'
                       
                    xpath = PORT_KEY_MD_XPATH % (names, direction, 
                                                 direction, event_type)
                    metadata_ids = root.xpath( xpath )

                    if not len(metadata_ids):
                        continue
                    
                    keys = root.xpath(KEY_XPATH % metadata_ids[0])
                    if not len(keys):
                        continue
                    
                    md.key = keys[0]
                    md.save()
                    
        
        for md in mds:
            last_datum = Data.objects.filter(metadata=md).order_by('time').reverse()[:1]
            if len(last_datum):
                last_time = int(time.mktime(last_datum[0].time.timetuple())) + 1
            else:
                last_time = int(time.time()) - window
                
            response = query_psservice(ma, SETUPDATA_REQUEST % (md.key, last_time))
            
            if response is None:
                # TODO: Check for errors
                continue
            
            for v in parse_snmp_response(response):
                Data.objects.create(metadata=md, time=v['timeValue'],
                                    value=v['value'], units=v['valueUnits'])

