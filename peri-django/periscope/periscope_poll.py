#!/usr/bin/env python

import sys
import os
import time

from multiprocessing import Process

sys.path.append('/opt/')
sys.path.append('/opt/periscope/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from periscope.measurements.lib.SNMPRequest import get_all_mp, get_all_ma

def poll_ma(period, window):
    while 1:
        get_all_ma("packrat.internet2.edu", "2010", "/perfSONAR_PS/services/snmp/ESCPSMA", period, window)
        time.sleep(window)

def poll_mp(period, window):
    while 1:
        get_all_mp('198.124.220.8','8075','/perfSONAR_PS/services/universal/mp',period,window)
        time.sleep(window)

period=600
ma_window=15
mp_window=30

p1 = Process(target=poll_ma, args=(period, ma_window))
p1.start()

p2 = Process(target=poll_mp, args=(period, mp_window))
p2.start()

    

