import json
import re
import time
import urllib
from datetime import datetime
from datetime import timedelta

from psapi.protocol import events
from django.views.decorators.cache import never_cache

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max


from periscope.measurements.models import Metadata, Data

from periscope.measurements.lib.SNMPQuery import get_urn_measurements, get_port_latest_inout
from periscope.measurements.models import Data, EventTypes, UrnStub, Metadata
from periscope.topology.models import Port, Node, NetworkObjectDescriptions, EventType
from periscope.monitoring.models import PathDataModel
from periscope.measurements.lib import query_measurements


def get_perfometer_data(request):
    """
    Return total Tx and Rx per site to used on ther perfometers
    """
    #try:
    #    id = request.GET['id']
    #except:
    #    print "no ID"

    Gbp10 = 1250000000.0
    
    port = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=TenGigabitEthernet9/1')
    inout = get_port_latest_inout(port)
    
    result = "{ \"BNL\": {\n"
    result += "\t\"Tx\":%.2f,\n"%(inout['Tx'] / Gbp10 * 100)
    result += "\t\"Rx\":%.2f\n"%(inout['Rx'] / Gbp10  * 100)
    result += "\t},\n"

    port = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=TenGigabitEthernet2/3')
    inout = get_port_latest_inout(port)
    
    result += "\"Ultralight\": {\n"
    result += "\t\"Tx\":%.2f,\n"%((inout['Tx'] / Gbp10) * 100)
    result += "\t\"Rx\":%.2f\n"%((inout['Rx'] / Gbp10)  * 100)
    result += "\t}\n}"

    return HttpResponse(result , mimetype="text/plain") #, mimetype="application/json")
   

def get_host_info(request):
    try:
        id = urllib.unquote(request.GET['id'])
        
        try:
            node = Node.objects.get(unis_id=id)
        except Node.DoesNotExist:
            return HttpResponse("Invalid ID", mimetype="text/plain")
        
        content = {}
        try:
            node_desc = NetworkObjectDescriptions.objects.get(networkobject=node).description.value
            content['os'] = re.findall(r'os=(.*?),', node_desc)[0]
            content['kernel'] = re.findall(r'kernel=(.*?),', node_desc)[0]
            content['memory'] = re.findall(r'memory=(.*?),', node_desc)[0]
            content['cpu'] = re.findall(r'cpu=(.*?),', node_desc)[0]
            content['cores'] = re.findall(r'cores=(.*?),', node_desc)[0]
            content['blob'] = re.findall(r'blob=(.*)', node_desc)[0]
        except:
            content['os'] = "N/A"
            content['kernel'] = "N/A"
            content['memory'] = "N/A"
            content['cpu'] = "N/A"
            content['cores'] = "N/A"
            content['blob'] = "Node description is not available"

        content['node_id'] = urllib.quote(id)

        return render_to_response('measurements/host_info.html', content,
                                  context_instance=RequestContext(request))
    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")

def get_res_chart(request):
    try:
        id = request.GET['id']
        event = request.GET['event']

        try:
            path = PathDataModel.objects.get(path_id=id)
        except (PathDataModel.DoesNotExist):
            return HttpResponse("Path ID not found.", mimetype="text/plain")     

        recv = EventType.objects.get(value='http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0')
        try:
            ptype = ContentType.objects.get_for_model(PathDataModel)
            metain = Metadata.objects.get(objectID=path.id, objectType=ptype, event_type=recv)
        except:
            return HttpResponse("No metadata found.", mimetype="text/plain")

        res = Data.objects.filter(metadata=md)
        if (len(res) < 1):
            return HttpResponse("No measurements found.", mimetype="text/plain")

        try:
            event = EventTypes.objects.get(event_type=event)
        except (EventTypes.DoesNotExist):
            return HttpResponse("Invalid Event type", mimetype="text/plain")
        
        return render_to_response('measurements/res_plot.html', {
            'id': id,
            'event': event,
        }, context_instance=RequestContext(request))
    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")


def get_dojo_chart_mongo(request):
    unis_id = urllib.unquote(request.GET.get('id', ''))
    event = request.GET.get('event', None)
    t = request.GET.get('t', 1800)
    if not unis_id:
        return HttpResponseBadRequest("UNIS ID is is not defined.")
    
    if not event:
        return HttpResponseBadRequest("Event type is is not defined.")
    
    return render_to_response('measurements/dojo_plot3.html', {
        'id': urllib.quote(unis_id),
        'in': 'recv',
        'out': 'sent',
        'event': event,
        't': 'time',
    }, context_instance=RequestContext(request))

    
def get_measurements_data_mongo(request):
    unis_id = urllib.unquote(request.GET.get('id', ''))
    event = request.GET.get('event', None)
    t = request.GET.get('t', 1800)
    try:
        t = int(t)
    except:
        return HttpResponseBadRequest("Time (t) must be an integer.")
    
    ganglia_sent = 'http://ggf.org/ns/nmwg/tools/ganglia/network/utilization/bytes/2.0'
    ganglia_recv = 'http://ggf.org/ns/nmwg/tools/ganglia/network/utilization/bytes/received/2.0'
    events_map = {}
    events_map[events.NET_DISCARD] = [events.NET_DISCARD_RECV, events.NET_DISCARD_SENT]
    events_map[events.NET_ERROR] = [events.NET_ERROR_RECV, events.NET_ERROR_SENT]
    events_map[events.NET_UTILIZATION] = [events.NET_UTILIZATION_RECV, events.NET_UTILIZATION_SENT]
    events_map[events.NET_UTILIZATION] = [ganglia_sent, ganglia_recv]
    
    if not unis_id:
        return HttpResponseBadRequest("UNIS is is not defined.")
    
    if not event:
        return HttpResponseBadRequest("Event type is is not defined.")

    if event not in events_map:
        return HttpResponseBadRequest("Invalid Event type")
    
    time_delta = timedelta(0, t)
    measurements = query_measurements(unis_id, events_map[event], None, 
        {'time': {
            '$gte': datetime.now() - time_delta, '$lte': datetime.now()
        }})
        
    values = ""
    labels = ""
    
    result = {"identifier": "event_type",
        "idAttribute": "event_type",
        "label": "timestamps", "items": []}
    
    for meta_id, meta in measurements['meta'].items():
        if meta['event_type'] == ganglia_sent:
            event = events.NET_UTILIZATION_SENT
        elif meta['event_type'] == ganglia_recv:
            event = events.NET_UTILIZATION_RECV
        else:
            event =  meta['event_type']
        tmp = {'urn': meta['unis_id'], 'event_type': event, "values":[], 'timestamps': []}
        for data in  measurements['data'][meta_id]:
            tmp['values'].append(data['value'])
            tmp['timestamps'].append(data['time'])
        result['items'].append(tmp)
    
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    return HttpResponse(json.dumps(result,  default=dthandler), mimetype="text/plain")
    
        

# TODO: 
def get_dojo_chart(request):
    #try:
    port_id = urllib.unquote(request.GET['id'])
    event = request.GET['event']
    t = request.GET['t']

    if event != 'http://ggf.org/ns/nmwg/characteristic/utilization/2.0':
        return HttpResponse("Invalid Event type", mimetype="text/plain")
    
    event_in = 'http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/received/2.0'
    event_out = 'http://ggf.org/ns/nmwg/characteristic/network/utilization/bytes/sent/2.0'
    try:
        port = Port.objects.get(unis_id=port_id)
        md_in = Metadata.objects.get(objectID=port.id, event_type__value=event_in)
        md_out = Metadata.objects.get(objectID=port.id, event_type__value=event_out)
    except:
        return HttpResponse("No data", mimetype="text/plain")
    
    return render_to_response('measurements/dojo_plot2.html', {
        'id': urllib.quote(port_id),
        'in': md_in.id,
        'out': md_out.id,
        'event': event,
        't':t,
    }, context_instance=RequestContext(request))
    #except (KeyError):
    #    return HttpResponse("Invalid Request", mimetype="text/plain")


def view_dojo_chart(request):
    try:
        urn = request.GET['urn']
        event = request.GET['event']

        return render_to_response('measurements/dojo_plot.html', {
            'urn': urn,
            'event': event,
        }, context_instance=RequestContext(request))
    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")


def get_host_data(request):
    from cStringIO import StringIO

    try:
        node_id = urllib.unquote(request.GET['id'])

        curr_time = int(time.time())
        last_two_min = datetime.fromtimestamp(float(curr_time - 1200))

        json_data = StringIO()
        json_data.write('[\n');

        node = Node.objects.get(unis_id=node_id)
        for md in Metadata.objects.filter(objectID=node.id):
            measurements = Data.objects.filter(metadata=md, time__gte=last_two_min)

            json_data.write('{eT: "%s", values: [' % md.event_type.value)

            for m in measurements:
                json_data.write('%s,' % m.value)

            json_data.write("], timestamps: [")

            for m in measurements:
                json_data.write('"%s",' % time.strftime("%H:%M:%S", m.time.timetuple()))

            json_data.write("]},\n");

        json_data.write(']');

        return HttpResponse(json_data.getvalue(), mimetype="application/json")

    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")


def get_res_data(request):
    from cStringIO import StringIO

    try:
        id = request.GET['id']
        event = request.GET['event']

        try:
            event = EventTypes.objects.get(event_type=event)
        except (EventTypes.DoesNotExist):
            return HttpResponse("Invalid Event type", mimetype="text/plain")

        measurements = Data.objects.filter(urn=id)
        
        json_data = StringIO() 
        json_data.write('[\n{urn: "%s", values: [' % id)

        for m in measurements:
            json_data.write('%s,' % m.value)

        json_data.write("], timestamps: [")

        for m in measurements:
            json_data.write('"%s",' % time.strftime("%H:%M:%S", m.time.timetuple()))
    
        json_data.write("]}\n]");
        return HttpResponse(json_data.getvalue(), mimetype="application/json")

    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")


def get_iface_data(request):
    try:
        md_in = request.GET['in']
        md_out = request.GET['out']
        t = request.GET['t']

        curr_time = int(time.time())
        start_t = datetime.fromtimestamp(float(curr_time - int(t)))

        values = ""
        labels = ""
 
        result = "{ \"identifier\": \"urn\", \"idAttribute\": \"urn\", \"label\": \"timestamps\", \"items\": [\n"
        
        result += "\t{\"urn\": \"%s\", \"values\":[" % md_in
        measurements = get_urn_measurements(md_in, start_t)
        
        for m in measurements:
            values += "%s,"%m.value
            labels += "'%s',"%time.strftime("%H:%M:%S", m.time.timetuple())

        result += values
        result += "], \"timestamps\":["
        result += labels
        result += "]},\n"
        
        result += "\t{\"urn\": \"%s\", \"values\":[" % md_out
        measurements = get_urn_measurements(md_out, start_t)
        values = ""
        labels = ""
        for m in measurements:
            values += "%s,"%m.value
            labels += "'%s',"%time.strftime("%H:%M:%S", m.time.timetuple())

        result += values
        result += "], \"timestamps\":["
        result += labels
        result += "]}\n]}"
        return HttpResponse(result, mimetype="application/json")

    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")


def get_measurements_data(request):
    try:
        urn = request.GET['urn']
        event = request.GET['event']
        
        try:
            event = EventTypes.objects.get(event_type=event)
        except (EventTypes.DoesNotExist):
            return HttpResponse("Invalid Event type", mimetype="text/plain")
        
        measurements = get_urn_measurements(urn, event)
        
        result = "{\n label:'%s',\ndata:[\n"%urn
        for m in measurements:
            result += "\t[%s,%s],\n"%(time.mktime(m.time.timetuple()), m.value)
        result = result[:-2] + "]\n}"
        return HttpResponse(result, mimetype="application/json")
        
    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")
        
        

def view_measurements_data(request):
    try:
        urn = request.GET['urn']
        event = request.GET['event']
        
        return render_to_response('measurements/plot2.html', {
            'urn': urn,
            'event': event,
        }, context_instance=RequestContext(request))
        
    except (KeyError):
        return HttpResponse("Invalid Request", mimetype="text/plain")
    
