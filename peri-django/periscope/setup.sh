rm database/periscope.sqlite
python manage.py syncdb
python manage.py loaddata initdata
python manage.py shell < examples/tps-2-shapes.py