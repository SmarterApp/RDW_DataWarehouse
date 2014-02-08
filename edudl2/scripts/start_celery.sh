#! /bin/sh

# use virtualenv to run python

# we pass --config_file path_and_name_of config file, so it counts as 2 arguments

if [ $# == 2 ]; then
    start_celery.py $1 $2;
else
    python start_celery.py ;
fi
    


