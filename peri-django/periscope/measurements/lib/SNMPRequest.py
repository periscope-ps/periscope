# TODO(AH): MARK FOR REMOVAL

import time
from datetime import datetime

from lxml import etree,objectify

from perfsonar.message import psMessageBuilder, psMessageReader

from periscope.measurements.lib.SimpleClient import SimpleClient
from periscope.measurements.models import UrnStub, EventTypes, Data, RawData, Units
from periscope.monitoring.models import PathDataModel

def makeSNMPMA_lamp_message(ifAddress, type, startTime=None, endTime=None):
    msg="""
<nmwg:message xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
              xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
              xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
              type="SetupDataRequest" id="SetupDataRequest1">

  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadata1">
    <netutil:subject xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
                     id="s-in-netutil-1">
      <psed:host xmlns:psed="http://ggf.org/ns/nmwg/tools/psed/2.0/">
        <psed:address type="ipv4">%s</psed:address>
        <psed:type>%s</psed:type>
      </psed:host>
    </netutil:subject>
    <nmwg:eventType>http://ggf.org/ns/nmwg/characteristic/utilization/2.0</nmwg:eventType>
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
    
    msg2="""
<nmwg:message xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
              xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
              xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
              type="SetupDataRequest" id="SetupDataRequest1">

  <nmwg:metadata xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
                 id="metadata1">
    <netutil:subject xmlns:netutil="http://ggf.org/ns/nmwg/characteristic/utilization/2.0/"
                     id="s-in-netutil-1">
      <nmwgt:interface xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/">
        <nmwgt:ifAddress type="ipv4">%s</nmwgt:ifAddress>
        <nmwgt:direction>%s</nmwgt:direction>
      </nmwgt:interface>
    </netutil:subject>
    <nmwg:eventType>http://ggf.org/ns/nmwg/characteristic/utilization/2.0</nmwg:eventType>
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

    if type == "in" or type == "out":
        return msg2 % (ifAddress, type, startTime)
    else:
        return msg % (ifAddress, type, startTime)
    

def makeSNMPMAmessage(ifAddress, ifName, ifIndex, startTime=None, endTime=None):
    psm = psMessageBuilder('SetupDataRequest1', 'SetupDataRequest')
                   
    interfaceData = {
             'ifAddress type="ipv4"':ifAddress,
             'ifName':ifName,
             'ifIndex':ifIndex,
    }
    
    metadataId = 'metadata.%s' % time.time()
    
    metaParams = {}
    if startTime != None:
        metaParams['startTime'] = startTime
    
    if endTime != None:
        metaParams['endTime'] = endTime
    
    psm.addMetadataBlock(metadataId,
                subject='s-in-netutil-1',
                subjectType='interface',
                subjectData=interfaceData,
                eventType='http://ggf.org/ns/nmwg/characteristic/utilization/2.0',
                params=metaParams,
                paramid='1')
    dataBlockId = 'data.%s' % time.time()
    psm.addDataBlock(dataBlockId, metadataIdRef=metadataId)
    
    return psm

def parse_snmp_response(response, type):
    """
    Parse the response from SNMP MA into array of values each element of the
    array is a dictionary of {timeValue, value, valueUnits}
    """
    values = []
    root = etree.fromstring(response)
    body = root.findall('{%s}Body'%'http://schemas.xmlsoap.org/soap/envelope/')
    for b in body:
        message = b.findall('{%s}message'%'http://ggf.org/ns/nmwg/base/2.0/')
        for m in message:
            data = m.findall('{%s}data'%'http://ggf.org/ns/nmwg/base/2.0/')
            for d in data:
                datum = d.findall('{%s}datum'%'http://ggf.org/ns/nmwg/base/2.0/')
                for d2 in datum:
                    #to check this is not an error message
                    if d2.text != '':
                        if d2.attrib['value'] != '' and d2.attrib['value'] != None and d2.attrib['value'] != 'nan':
                            v = {}
                            v['timeValue'] =  datetime.fromtimestamp(float(d2.attrib['timeValue']))
                            v['value']=d2.attrib['value']
                            if type!="lamp":
                                v['valueUnits'] = d2.attrib['valueUnits']
                            values.append(v)

    return values                                          
                     

def get_all_ma(host, port, uri, period, window=None, type="default"):
    """
    Get all values measurements values from the measurement archive.
    """
    urns = UrnStub.objects.filter(source="MA")
    
    curr_time = int(time.time())

    if (window == None):
        start = curr_time - period
        drop_time = datetime.fromtimestamp(float(start))
    else:
        start = curr_time - window
        drop_time = datetime.fromtimestamp(float(curr_time - period))
    
    print "Getting new data for ma", datetime.fromtimestamp(float(start)), "to", datetime.fromtimestamp(float(curr_time)) 

    for u in urns:
        
        if (type == "lamp"):
            body = makeSNMPMA_lamp_message(ifAddress=u.ifAddress, type=u.type, startTime=start)
        else:
            body = makeSNMPMAmessage(ifAddress=u.ifAddress, ifIndex=u.ifIndex, ifName=u.ifName, startTime=start)    

        response=None

        try:
            client = SimpleClient(host=host, port=port, uri=uri)
            if type == "lamp":
                response = client.send_request(body)
            else:
                response = client.send_request(body.tostring())
        except:
            print "could not poll ma!"
            continue

        values = parse_snmp_response(response, type)
        
        event = EventTypes.objects.get(event_type='http://ggf.org/ns/nmwg/characteristic/utilization/2.0')
        
        unit= None
        if len(values) > 0:
            if type=="lamp":
                unit = Units.objects.get(unit="psed")
            else:
                unit = Units.objects.get(unit=values[0]['valueUnits'])
            
        for v in values:
            m = Data(urn=u.urn, event_type=event, time=v['timeValue'], value=v['value'], units=unit)
            m.save()

    measurement_data = Data.objects.filter(time__lt=drop_time)
    for data in measurement_data:
        data.delete()

    print "Dropped measurements older than", drop_time


msg_mp="""
<nmwg:message type="MeasurementRequest" id="msg1"
        xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/"
        xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/"
	xmlns:command="http://ggf.org/ns/nmwg/tools/command/2.0/">

<nmwg:metadata id="CiscoSSHRequest">
	<command:subject id="sub1">
		<nmwgt:endPointPair>
			<nmwgt:dst type="dst" value="%s" />
		</nmwgt:endPointPair>
	</command:subject>
	<nmwg:eventType>http://ggf.org/ns/nmwg/tools/ciscossh/2.0/</nmwg:eventType>
	<command:parameters id="param1">
		<nmwg:parameter name="command" value="%s" />
		<nmwg:parameter name="argument" value="%s"/>
	</command:parameters>
</nmwg:metadata>
<nmwg:data id="1" metadataIdRef="CiscoSSHRequest" />
</nmwg:message>
"""

def get_all_mp(host, port, uri,period, window=None):
    """
    Get all values measurements values from the measurement point.
    """
    urns = UrnStub.objects.all()
    active_paths = PathDataModel.objects.filter(status="active");

    if (len(active_paths) < 1):
        return

    curr_time = int(time.time())
    
    if (window == None):
        start = curr_time - period
        drop_time = datetime.fromtimestamp(float(start))
    else:
        start = curr_time - window
        drop_time = datetime.fromtimestamp(float(curr_time - period))

    print "Getting new data for mp", datetime.fromtimestamp(float(start)), "to", datetime.fromtimestamp(float(curr_time)) 

    # this is horrible, but for now we assume the only interface we monitor is netqos02->qtr2 (GigabitEthernet9/23)
    # eventually we need a clean way to get the interface that the MP should query based on the path source
    for a in active_paths:
        ids = a.path_id
        ids += " GigabitEthernet9/23"

        #ids = ids[:-1]

        mp_query = msg_mp % ("198.124.220.3", "show terapaths", ids)

        try:
            client = SimpleClient(host=host, port=port, uri=uri)
            response = client.send_request(mp_query)
        except: 
            print "could not poll mp!"
            return

        reader= psMessageReader(response)
        values = []
        for i in reader.getDataBlockIds():
            d = reader.getData(i)
            values = d.datumValues
                
            event = EventTypes.objects.get(event_type='http://ggf.org/ns/nmwg/tools/ciscossh/2.0/')
            
            unit = None
            if len(values) > 0:
                unit = Units.objects.get(id=0)
                
                # the MP is now returning packets that matched the policy-map on Qtr2
                # Qtr1 gives bytes in the reverse direction only...*sigh*
                # MTU is 1500, so we do some rough calculation to get bytes
                i = 0              
                for v in values:
                    rate=None
                    prev=None

                    try:
                        prev = RawData.objects.filter(urn=a.path_id).latest('time')
                    except (RawData.DoesNotExist):
                        print "no previous raw path measurement"

                    if ((not prev) or (v['value'] == 0)):
                        rate = 0
                    elif (v['value'] < prev.value):
                        rate = 0
                    else:
                        if ((float(curr_time) - time.mktime(prev.time.timetuple())) < 30):
                            return
                        rate = ((float(v['value'])-float(prev.value))*1500)/(float(v['timeValue'])-time.mktime(prev.time.timetuple()))
                        
                    m = Data(urn=a.path_id, 
                             event_type=event, 
                             time=datetime.fromtimestamp(float(v['timeValue'])),
                             value=rate,
                             units=unit)
                    m.save()

                    m = RawData(urn=a.path_id,
                                event_type=event,
                                time=datetime.fromtimestamp(float(v['timeValue'])),
                                value=v['value'],
                                units=unit)

                    m.save()
