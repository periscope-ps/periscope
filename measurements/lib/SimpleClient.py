from httplib import HTTPConnection, HTTPSConnection

class SimpleClient:
    """
    Very simple client to send SOAP requests to perfSONAR service
    """

    def __init__(self, host, port, uri, cert=None, key=None):
        self.host = host
        self.port = port
        self.uri  = uri
        self.cert = cert
        self.key = key
    
    def soapifyMessage(self, message):
        headerString = """<SOAP-ENV:Envelope 
 xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Header/>
<SOAP-ENV:Body>
%s
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
""" % message
        return headerString

    def send_request(self, message, useSSL=False, issoap=False):
        if useSSL:
            conn = HTTPSConnection(self.host, self.port, self.key, self.cert)
        else:
            conn = HTTPConnection(self.host, self.port)
            
        conn.connect()
        headers = {'SOAPAction':'', 'Content-Type': 'text/xml'}
        if issoap == False:
            message = self.soapifyMessage(message)
        conn.request('POST', self.uri, message, headers)
        resp = conn.getresponse()
        response = resp.read()
        conn.close() 
        return response

