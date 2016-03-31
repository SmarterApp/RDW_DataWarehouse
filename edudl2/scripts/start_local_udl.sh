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


#python ../../config/generate_ini.py -i ../../config/udl2_conf.yaml -o /opt/edware/conf/udl2_conf.ini
sh teardown_udl2_database.sh
sh initialize_udl2_database.sh
sh start_celery.sh
