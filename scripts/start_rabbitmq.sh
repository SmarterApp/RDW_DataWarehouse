#! /bin/sh

# I set up my virtualenv for python3.3 under ~/ejen/py33/bin

source ~/py33/bin/activate
if [ $1 ]; then
    start_rabbitmq.py;
else
    start_rabbitmq.py $1;
fi