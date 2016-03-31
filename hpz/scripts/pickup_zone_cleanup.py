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

import argparse
from hpz.utils.maintenance import cleanup
from hpz.database.hpz_connector import initialize_db
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
__author__ = 'smuhit'


parser = argparse.ArgumentParser(description='Cleanup HTTP pickup zone files and database')
parser.add_argument('-c', '--config', help="The path to the HTTP pickup zone ini file",
                    default="/opt/edware/conf/hpz.ini")
args = parser.parse_args()
config = ConfigParser()
config.read(args.config)
settings = config['app:main']

initialize_db(settings)
cleanup(settings)
