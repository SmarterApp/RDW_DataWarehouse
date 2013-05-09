#! /bin/sh

# I set up my virtualenv for python3.3 under ~/ejen/py33/bin

start_rabbitmq.sh
sleep 1
start_celery.sh
