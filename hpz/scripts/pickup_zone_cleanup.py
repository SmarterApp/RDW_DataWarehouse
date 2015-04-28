from hpz.utils.maintenance import cleanup
from hpz.database.hpz_connector import initialize_db
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
__author__ = 'smuhit'


import argparse

parser = argparse.ArgumentParser(description='Cleanup HTTP pickup zone files and database')
parser.add_argument('-c', '--config', help="The path to the HTTP pickup zone ini file",
                    default="/opt/edware/conf/hpz.ini")
args = parser.parse_args()

config = ConfigParser()
config.read(args.config)

settings = config['app:main']
initialize_db(settings)
record_expiration = settings.get('hpz.record_expiration', 30)

cleanup(record_expiration)
