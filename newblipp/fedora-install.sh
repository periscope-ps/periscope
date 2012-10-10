#!/bin/bash
#
# Self-extracting bash script that installs blipp
#
# create self extracting tarball like this (from parent dir): 
# 'tar zc blipp | cat blipp/fedora-install.sh - > blipp.sh'
# Supports: Debian based distributions
# Depends: python 2.6

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

SKIP=`awk '/^__TARFILE_FOLLOWS__/ { print NR + 1; exit 0; }' $0`
THIS=`pwd`/$0
tail -n +$SKIP $THIS | tar -xz

# Installation steps for LAMP Toolkit
DIR=newblipp
ETC=/usr/local/etc

yum -y install python-setuptools
yum -y install libnl-devel
cd ${DIR}
python ./setup.py install 

exit 0

__TARFILE_FOLLOWS__
