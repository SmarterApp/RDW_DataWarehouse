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

from ast import literal_eval
__author__ = 'sravi'
from edmigrate.utils.constants import Constants


class Config():
    BROADCAST_QUEUE = 'migrate.broadcast.queue'
    LAG_TOLERENCE_IN_BYTES = 'migrate.lag_tolerence_in_bytes'
    IPTABLES_CHAIN = 'migrate.iptables.chain'
    IPTABLES_SUDO = 'migrate.iptables.sudo'
    IPTABLES_COMMAND = 'migrate.iptables.command'
    DEFAULT_ROUTUNG_KEY = 'migrate.celery.CELERY_DEFAULT_ROUTING_KEY'
    DEFAULT_ROUTUNG_QUEUE = 'migrate.celery.CELERY_DEFAULT_ROUTING_QUEUE'
    BROKER_URL = 'migrate.celery.BROKER_URL'
    BROKER_USE_SSL = 'migrate.celery.BROKER_USE_SSL'
    EAGER_MODE = 'migrate.celery.celery_always_eager'


# list of configurations that are specific to edmigrate
LIST_OF_CONFIG = [(Config.BROADCAST_QUEUE, str, None),
                  (Config.LAG_TOLERENCE_IN_BYTES, int, 10),
                  (Config.DEFAULT_ROUTUNG_KEY, str, Constants.WORKER_NAME),
                  (Config.DEFAULT_ROUTUNG_QUEUE, str, Constants.CONDUCTOR_QUEUE),
                  (Config.BROKER_URL, str, 'memory://'),
                  (Config.EAGER_MODE, bool, False),
                  (Config.BROKER_USE_SSL, literal_eval, '{}'),
                  (Config.IPTABLES_CHAIN, str, Constants.IPTABLES_CHAIN),
                  (Config.IPTABLES_COMMAND, str, Constants.IPTABLES_COMMAND),
                  (Config.IPTABLES_SUDO, str, Constants.IPTABLES_SUDO)]


# Keeps track of configuration related to edmigrate that is read off from ini
settings = {}


def setup_settings(config):
    '''
    Reads a dictionary of values, and saves the relevant ones to settings

    :param dict config:  dictionary of configuration for application
    '''
    global settings
    for item in LIST_OF_CONFIG:
        key = item[0].lower()
        to_type = item[1]
        default = item[2]
        settings[key] = to_type(config.get(key, default))


def get_setting(key, default_value=None):
    '''
    Given a key, look up value in settings

    :params string key:  lookup key
    '''
    return settings.get(key.lower(), default_value)
