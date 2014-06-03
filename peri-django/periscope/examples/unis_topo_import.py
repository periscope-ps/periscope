from django.conf import settings
from periscope.topology.models import *
from periscope.topology.lib.topology import create_from_xml_file
from periscope.topology.lib.util import save_parsed_elements

t = create_from_xml_file(settings.PERISCOPE_ROOT + "examples/escps-unis.xml")
save_parsed_elements(t[0])
