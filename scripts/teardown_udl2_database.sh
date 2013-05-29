#!/bin/sh

# use virtualenv to run initialization script

python -m udl2.database $1 $2 --action teardown 
