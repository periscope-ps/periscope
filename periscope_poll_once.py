#!/usr/bin/env python

import sys
import os
import time

sys.path.append('/opt/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from periscope.measurements.lib.SNMPRequest import get_all_mp, get_all_ma

period=600
window=30

get_all_ma("packrat.internet2.edu", "2010", "/perfSONAR_PS/services/snmp/ESCPSMA", period, window)
get_all_mp('198.124.220.8','8075','/perfSONAR_PS/services/universal/mp',period,window)
