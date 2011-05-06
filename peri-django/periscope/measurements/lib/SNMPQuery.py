from django.db.models import Max

from periscope.measurements.models import UrnStub, EventTypes, Data, Units, Metadata
from periscope.topology.models import *
from django.contrib.contenttypes.models import ContentType


def get_port_latest_inout(port):
    """
    Get the latest values of Tx and Rx of the specified port.
    The return value is a dict of {'Tx': value, 'RX': value}
    """

    sent = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0')
    recv = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0')
    
    ptype = ContentType.objects.get_for_model(Port)
    
    metain = Metadata.objects.get(objectID=port.id, objectType=ptype, event_type=recv)
    metaout = Metadata.objects.get(objectID=port.id, objectType=ptype, event_type=sent)
        
    last_datum = Data.objects.filter(metadata=metain).order_by('time').reverse()[:1][0]
    rx_value = last_datum.value

    last_datum = Data.objects.filter(metadata=metaout).order_by('time').reverse()[:1][0]
    tx_value = last_datum.value

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
