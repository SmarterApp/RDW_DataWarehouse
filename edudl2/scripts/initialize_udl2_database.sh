#!/bin/sh
# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.


# initialize edware star schema

python3.3 -m edschema.metadata_generator --metadata stats -s edware_stats -d edware_stats --host=localhost:5432 -u edware -p edware2013

# Create prod schema
python3.3 -m edschema.metadata_generator --metadata edware -s edware_prod -d edware --host=localhost:5432 -u edware -p edware2013
# Load data into prod
python3.3 populate_prod_database.py

# use virtualenv to run initialization script
# otherwise, it must be python3.3

python3.3 -m edudl2.database.database $1 $2 --action setup
