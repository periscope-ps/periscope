from lxml import etree
from datetime import datetime

def parse_snmp_response(response):
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
                            v['valueUnits'] = d2.attrib['valueUnits']
                            values.append(v)

    return values

def parse_snmp_response_data(data):
    """
    Parse the response from SNMP MA into array of values each element of the
    array is a dictionary of {timeValue, value, valueUnits}
    """
    values = []
    datum = data.findall('{%s}datum'%'http://ggf.org/ns/nmwg/base/2.0/')
    for d2 in datum:
        #to check this is not an error message
        if d2.text != '':
            if d2.attrib['value'] != '' and d2.attrib['value'] != None and d2.attrib['value'] != 'nan':
                v = {}
                v['timeValue'] =  datetime.fromtimestamp(float(d2.attrib['timeValue']))
                v['value']=d2.attrib['value']
                v['valueUnits'] = d2.attrib['valueUnits']
                values.append(v)
    
    return values
