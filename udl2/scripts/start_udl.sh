#! /bin/sh
# The script acceptes --config_file path_and_name_of config file, so it counts as 2 arguments

if [ $# == 2 ]; then
    start_rabbitmq.sh $1 $2
    sleep 10
    start_celery.sh $1 $2;
else # use default values that should be in /opt/wgen/edware-udl/udl2_conf.py
   start_rabbitmq.sh
   sleep 1 
   start_celery.sh $
fi
