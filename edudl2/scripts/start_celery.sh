#! /bin/sh
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


# use virtualenv to run python

# we pass --config_file path_and_name_of config file, so it counts as 2 arguments

# remove outstanding failed celery tasks

celeryctl purge

if [ $# == 2 ]; then
    start_celery.py $1 $2;
else
    python start_celery.py ;
fi
    


