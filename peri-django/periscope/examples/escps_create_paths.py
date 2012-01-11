#!/usr/bin/env python

from django.conf import settings
from periscope.topology.models import *
from django.contrib.contenttypes.models import ContentType


escps_paths = {}
escps_paths['netqos03'] = {}
escps_paths['netqos03']['tera04'] = ['ex2500-netqos03', 'qtr1-ex2500', 'nile-tera04']
escps_paths['netqos03']['tera05'] = ['ex2500-netqos03', 'qtr1-ex2500', 'nile-tera05']

escps_paths['netqos04'] = {}
escps_paths['netqos04']['tera04'] = ['netqos04-ex2500', 'ex2500-netqos04', 'qtr1-ex2500', 'nile-tera04']
escps_paths['netqos04']['tera05'] = ['netqos04-ex2500', 'ex2500-netqos04', 'qtr1-ex2500', 'nile-tera05']

escps_paths['udel02'] = {}
escps_paths['udel02']['tera04'] = ['udel02-sw-udel', 'nile-tera04']
escps_paths['udel02']['tera05'] = ['udel02-sw-udel', 'nile-tera05']
escps_paths['udel02']['netqos03'] = ['udel02-sw-udel', 'qtr1-ex2500', 'ex2500-netqos03']
escps_paths['udel02']['netqos04'] = ['udel02-sw-udel', 'qtr1-ex2500', 'ex2500-netqos04']

Path.objects.all().delete()

def create_paths(paths):
    for src in paths:
        for dst in paths[src]:
            path_id = "%s2%s" % (src, dst)
            print "PATH: %s -> %s" % (src, dst)
            path = Path(unis_id=path_id)
            path.save()
        
            for linkid in paths[src][dst]:
                print linkid
                link =  Link.objects.filter(unis_id__contains=linkid)
                
                hop_id = "%sto%s" % (src, dst)
                hop = Hop(unis_id=hop_id, parent=path, target=link[0])
                hop.save()

create_paths(escps_paths)
