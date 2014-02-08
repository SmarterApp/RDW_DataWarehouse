#!/bin/sh

# use virtualenv to run initialization script

python -m udl2.database $1 $2 --action teardown 

# teardown edware star schema

python3.3 -m edschema.metadata_generator --metadata edware -a teardown -s edware -d edware --host=localhost:5432 -u edware -p edware2013