#!/bin/sh
#
# Attempt to automate install of JQuery
#
tmpdir=JQuery_Download
mkdir $tmpdir
cd $tmpdir

# JQuery
jqver=1.7
jqcode=http://code.jquery.com
jqname=jquery-${jqver}.min.js
jqlink=$jqcode/$jqname
wget $jqlink
cp $jqname ../static/js/jquery.min.js

# JQuery-UI
jquver=1.8.20
jqucode=http://jqueryui.com/download
jquname=jquery-ui-${jquver}.custom.zip
jqulink=$jqucode/$jquname
wget $jqulink
unzip $jquname
cp js/jquery-ui-*.*.*.custom.min.js ../static/js/jquery-ui.custom.min.js

mkdir -p css/ui-lightness ; cd css/ui-lightness
wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.3/themes/ui-lightness/jquery-ui.css
cd ../..
cp -r css/ui-lightness ../static/css/ui-lightness

# Cleanup
cd ..
#rm -rf $tmpdir
printf "Installation complete\n"
