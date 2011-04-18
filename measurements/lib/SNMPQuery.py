from django.db.models import Max

from periscope.measurements.models import UrnStub, EventTypes, Data, Units, Metadata
from periscope.topology.models import *
from django.contrib.contenttypes.models import ContentType


def get_node_latest_inout(node):
    """
    Get the latest values of Tx and Rx of the specified node.
    The return value is a dict of {'Tx': value, 'RX': value}
    """
    urns = UrnStub.objects.filter(urn__startswith=node)
    tx_value = 0
    rx_value = 0
    if len(urns) > 0:
        for u in urns:
            tx = []
            rx = []
            # make list of in and out ports of the node
            if u.urn[-3:] == '-in':
                rx.append(u.urn)
            elif u.urn[-4:] == '-out':
                tx.append(u.urn)
            
            for t in tx:
                time_max = Data.objects.filter(urn=t).aggregate(Max('time'))['time__max']
                tx_value += Data.objects.get(urn=t, time=time_max).value
                
            for r in rx:
                time_max = Data.objects.filter(urn=r).aggregate(Max('time'))['time__max']
                rx_value += Data.objects.get(urn=r, time=time_max).value
                            
    return {'Tx': tx_value, 'Rx': rx_value}
    


def get_port_latest_inout(port):
    """
    Get the latest values of Tx and Rx of the specified node.
    The return value is a dict of {'Tx': value, 'RX': value}
    """
    #urns = UrnStub.objects.filter(urn__startswith=node)
    sent = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0')
    recv = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0')
    
    ptype = ContentType.objects.get_for_model(Port)
    
    metain = Metadata.objects.get(objectID=port.id, objectType=ptype, event_type=recv)
    metaout = Metadata.objects.get(objectID=port.id, objectType=ptype, event_type=sent)
    
    
    tx_value = 0
    rx_value = 0
    if len(urns) > 0:
        for u in urns:
            tx = []
            rx = []
            # make list of in and out ports of the node
            if u.urn[-3:] == '-in':
                rx.append(u.urn)
            elif u.urn[-4:] == '-out':
                tx.append(u.urn)
            
            for t in tx:
                time_max = Data.objects.filter(metadata=metaout).aggregate(Max('time'))['time__max']
                tx_value += Data.objects.get(metadata=metaout, time=time_max).value
                
            for r in rx:
                time_max = Data.objects.filter(metadata=metain).aggregate(Max('time'))['time__max']
                rx_value += Data.objects.get(metadata=metain, time=time_max).value
                            
    return {'Tx': tx_value, 'Rx': rx_value}
    
    
    

def get_urn_measurements(metadata_id, start_time=None, end_time=None):
    """
    Query the database for specific even for network object.
    
    Optional Parameters are start_time and end_time.
    """
    
    measurements = None   
 
    if start_time == None and end_time == None:
        measurements = Data.objects.filter(metadata__pk=metadata_id)
    if start_time != None and end_time == None:
        measurements = Data.objects.filter(metadata__pk=metadata_id,
                                                   time__gte=start_time)
    if start_time == None and end_time != None:
        measurements = Data.objects.filter(metadata__pk=metadata_id,
                                                   time__lte=end_time)
    if start_time != None and end_time != None:
                measurements = Data.objects.filter(metadata__pk=metadata_id,
                                                   time__gte=start_time,
                                                   time__lte=end_time)
    return measurements
