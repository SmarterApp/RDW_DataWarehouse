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


# use virtualenv to run initialization script

python -m edudl2.database.database $1 $2 --action teardown

# teardown edware star schema

python3.3 -m edschema.metadata_generator --metadata stats -a teardown -s edware_stats -d edware_stats --host=localhost:5432 -u edware -p edware2013

python3.3 -m edschema.metadata_generator --metadata edware -a teardown -s edware_prod -d edware --host=localhost:5432 -u edware -p edware2013
