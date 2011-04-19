import urllib
import time
from datetime import datetime

import re

from django.views.decorators.cache import never_cache


from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max


from periscope.measurements.models import Metadata, Data

from periscope.measurements.lib.SNMPQuery import get_urn_measurements, get_node_latest_inout, get_port_latest_inout
from periscope.measurements.models import Data, EventTypes, UrnStub, Metadata
from periscope.topology.models import Port, Node, NetworkObjectDescriptions
from periscope.monitoring.models import PathDataModel


def get_perfometer_data(request):
    """
    Return total Tx and Rx per site to used on ther perfometers
    """
    #try:
    #    id = request.GET['id']
    #except:
    #    print "no ID"

    Gbp10 = 1250000000.0
    
    port = Port.objects.get(unis_id='urn:ogf:network:domain=ps.es.net:node=bois-cr1:port=xe-0/0/0')
    inout = get_port_latest_inout(port)
    
    #bnl = get_node_latest_inout('qtr1-Te9/1')
    result += "{\"Tx\":%.2f,\n"%(bnl['Tx'] / Gbp10 * 100)
    result += "\t\"Rx\":%.2f\n"%(bnl['Rx'] / Gbp10  * 100)
    result += "},"
    
    return HttpResponse(result , mimetype="text/plain") #, mimetype="application/json")
    
    #result = "{ \"BNL\": {\n"
    #result += "\t\"Tx\":%.2f,\n"%(bnl['Tx'] / Gbp10 * 100)
    #result += "\t\"Rx\":%.2f\n"%(bnl['Rx'] / Gbp10  * 100)
    #result += "\t},\n"
    
    #Ultralight = get_node_latest_inout('nile-Te2/1')
    #result += "\"Ultralight\": {\n"
    #result += "\t\"Tx\":%.2f,\n"%((Ultralight['Tx'] / Gbp10) * 100)
    #result += "\t\"Rx\":%.2f\n"%((Ultralight['Rx'] / Gbp10)  * 100)
    #result += "\t}\n}"
    return HttpResponse(result , mimetype="text/plain") #, mimetype="application/json")
   


def get_host_info(request):
    from cStringIO import StringIO

    try:
        id = request.GET['id']
        
        node_name = re.findall(r'node=(.*)', id)
        
        if len(node_name) > 0:
            urns = UrnStub.objects.filter(ifHost=node_name[0])
        else:
            return HttpResponse("Invalid ID", mimetype="text/plain")
        
        if len(urns) < 1 :
            return HttpResponse("No data", mimetype="text/plain")
        
        node = Node.objects.filter(names__value=node_name[0])

        if node:
            node_desc = NetworkObjectDescriptions.objects.get(networkobject=node[0]).description.value

        content = {}
        #content['os'] = re.findall(r'os=(.*?),', node_desc)[0]
        #content['kernel'] = re.findall(r'kernel=(.*?),', node_desc)[0]
        #content['memory'] = re.findall(r'memory=(.*?),', node_desc)[0]
        #content['cpu'] = re.findall(r'cpu=(.*?),', node_desc)[0]
        #content['cores'] = re.findall(r'cores=(.*?),', node_desc)[0]
        #content['blob'] = re.findall(r'blob=(.*)', node_desc)[0]

        content['os'] = "N/A"
        content['kernel'] = "N/A"
        content['memory'] = "N/A"
        content['cpu'] = "N/A"
        content['cores'] = "N/A"
        content['blob'] = "Node description is not available"

        i=0
        for u in urns:
            content['urn'+str(i)] = u.urn
            i += 1
 
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

        res = Data.objects.filter(urn=id)
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
        urn0 = request.GET['urn0']
        urn1 = request.GET['urn1']
        urn2 = request.GET['urn2']
        urn3 = request.GET['urn3']

        urns = [urn0, urn1, urn2, urn3]

        curr_time = int(time.time())
        last_two_min = datetime.fromtimestamp(float(curr_time - 120))

        json_data = StringIO()
        json_data.write('[\n');

        for i in range(4):
            if (urns[i]):
                measurements = Data.objects.filter(urn=urns[i], time__gte=last_two_min)
                json_data.write('{urn: "%s", values: [' % urns[i])
                
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
        #measurements = get_urn_measurements(id, event)	

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
    
