import os
import sys

sys.path.append('/opt/periscope/peri-django/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'periscope.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
sys.path.append('/opt')
