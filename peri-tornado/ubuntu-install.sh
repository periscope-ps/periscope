#!/bin/bash
#
# Self-extracting bash script that installs UNIS and the MS
#
# create self extracting tarball like this (from parent dir): 
# 'tar zc peri-tornado | cat peri-tornado/ubuntu-install.sh - > peri-tornado.sh'
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
DIR=peri-tornado

GENSOURCES_FILE="/etc/apt/sources.list.d/10gen.list"
GEN_REPO="deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen"
echo ${GEN_REPO} >> ${GENSOURCES_FILE}
sudo apt-get update
sudo apt-get install mongodb-10gen

#git clone git://github.com/ahassany/asyncmongo.git
#cd asyncmongo
#sudo python setup.py install
#cd ..

apt-get install libnl-dev
cd ${DIR}
python ./setup.py install 

exit 0

__TARFILE_FOLLOWS__
