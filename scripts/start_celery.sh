#! /bin/sh

# I set up my virtualenv for python3.3 under ~/py33/bin

source ~/py33/bin/activate

# we pass --config_file path_and_name_of config file, so it counts as 2 arguments

if [ $# == 2 ]; then
    start_celery.py $1 $2;
else
    start_celery.py ;
fi
    


