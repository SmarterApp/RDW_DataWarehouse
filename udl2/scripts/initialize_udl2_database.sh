#!/bin/sh

# initialize edware star schema

python3.3 -m edschema.metadata_generator --metadata edware -s edware -d edware --host=localhost:5432 -u edware -p edware2013

python3.3 -m edschema.metadata_generator --metadata stats -s edware_stats -d edware_stats --host=localhost:5432 -u edware -p edware2013


# use virtualenv to run initialization script
# otherwise, it must be python3.3

python3.3 -m udl2.database $1 $2 --action setup

