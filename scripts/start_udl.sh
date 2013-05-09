#! /bin/sh

# I set up my virtualenv for python3.3 under ~/ejen/py33/bin

if [ $1 ]; then
   start_rabbitmq.sh
   sleep 1
   start_celery.sh;
else
   start_rabbitmq.sh $1
   sleep 1 
   start_celery.sh $1;
fi
