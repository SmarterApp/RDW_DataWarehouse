#!/bin/sh

# Use virtualenv or python 3.3 to run teardown script
# Teardown HPZ database

python3.3 -m hpz.database.metadata_generator --metadata hpz -a teardown -s hpz -d hpz --host=localhost:5432 -u hpz -p hpz2014
