#! /bin/sh

# Setting up my virtualenv for python3.3 

# we pass --config_file path_and_name_of config file, so it counts as 2 arguments

if [ $# == 2 ]; then
    start_rabbitmq.py $1 $2;
else
    start_rabbitmq.py;
fi
