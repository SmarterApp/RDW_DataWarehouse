#!/bin/sh

# use virtualenv to run initialization script
# otherwise, it must be python3.3

python3.3 -m udl2.database $1 $2 --action setup
