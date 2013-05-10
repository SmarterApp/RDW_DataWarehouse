#!/bin/sh

# use virtualenv to run initialization script
source ~/py33/bin/activate

# check postgres can be use by user

if [ "`which createuser`" == '' ]; then
    echo "You don't have postgres access"
    exit
fi

initialize_udl2_database.py