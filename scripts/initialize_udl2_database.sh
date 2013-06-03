#!/bin/sh

# use virtualenv to run initialization script
# otherwise, it must be python3.3

python3.3 -m udl2.database $1 $2 --action setup

# initialize edware star schema

python3.3 -m edschema.ed_metadata -s edware -d edware --host=localhost:5432 -u edware -p edware2013