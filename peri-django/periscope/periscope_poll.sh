#!/bin/bash

dt=15
while true;
  do
   now=`date +%s`
   left=`expr ${dt} - \( ${now}  % ${dt} \)`
   sleep $left
   cd /opt/periscope
   /usr/bin/python /opt/periscope_ani/peri-django/periscope/manage.py pull all
  done
