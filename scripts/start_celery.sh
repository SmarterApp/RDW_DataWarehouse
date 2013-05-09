#! /bin/sh

# I set up my virtualenv for python3.3 under ~/ejen/py33/bin

source ~/py33/bin/activate
if [ $1 ]; then
    start_celery.py;
else
    start_celery.py $1;
fi
    


