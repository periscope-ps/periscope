import base64

from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers import primitive as soap_types
 
from django.conf import settings
from django.http import HttpResponse
 
def extract_basic_credentials(request):
    username, password = None, None
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                username, password = base64.b64decode(auth[1]).split(':')
    return username, password
 
class Http401(Exception):
    pass
 
class Http403(Exception):
    pass
 
class DjangoSoapApp(SimpleWSGISoapApp):
 
    def authenticate(self, request):
        ws_username = getattr(settings, 'WS_USERNAME', None)
 
        if ws_username:
            ws_password = getattr(settings, 'WS_PASSWORD', None)
            username, password = extract_basic_credentials(request)
 
            if username == None:
                raise Http401("401 Authentication required.")
 
            if username != ws_username or password != ws_password:
                raise Http403("403 Not authorized")
 
    def __call__(self, request):
        self.authenticate(request)
        django_resp = HttpResponse()
 
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_resp.status_code = int(status)
 
            for header, value in headers:
                django_resp[header] = value
 
        response = super(SimpleWSGISoapApp, self).__call__(request.META, start_response)
        django_resp.content = "\n".join(response)
        return django_resp
        if django_resp.status_code == 405:
            return HttpResponse("405 Method not allowed.", 'text/plain', status=405)
