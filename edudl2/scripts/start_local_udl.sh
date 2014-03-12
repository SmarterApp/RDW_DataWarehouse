#!/bin/sh

python ../../config/generate_ini.py -i ../../config/udl2_conf.yaml -o /opt/edware/conf/udl2_conf.ini
sh teardown_udl2_database.sh
sh initialize_udl2_database.sh
sh start_celery.sh
