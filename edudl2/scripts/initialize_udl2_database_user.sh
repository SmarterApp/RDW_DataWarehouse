#!/bin/sh

# use virtualenv to run initialization script

# check postgres can be use by user

if [ "`which createuser`" == '' ]; then
    echo "You don't have postgres access"
    exit
fi

initialize_udl2_database_user.py $1 $2 $3 $4
