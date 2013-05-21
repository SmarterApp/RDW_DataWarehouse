#!/bin/sh

# use virtualenv to run initialization script
#source ~/py33/bin/activate

python3.3 -m udl2.database $1 $2 --action setup
