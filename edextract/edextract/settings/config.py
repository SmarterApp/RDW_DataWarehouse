'''
Created on Nov 8, 2013

@author: dip
'''


class Config():
    MAX_RETRIES = 'extract.retries_allowed'
    RETRY_DELAY = 'extract.retry_delay'
    TIMEOUT = 'extract.timeout'

# list of configurations that are specific to edextract
LIST_OF_CONFIG = [(Config.MAX_RETRIES, int, 1),
                  (Config.RETRY_DELAY, int, 60),
                  (Config.TIMEOUT, int, 20),
                  ]

# Keeps track of configuration related to edextract that is read off from ini
settings = {}


def setup_settings(config):
    '''
    Reads a dictionary of values, and saves the relevant ones to settings

    :param dict config:  dictionary of configuration for application
    '''
    global settings
    for item in LIST_OF_CONFIG:
        key = item[0]
        to_type = item[1]
        default = item[2]
        settings[key] = to_type(config.get(key, default))


def get_setting(key):
    '''
    Given a key, look up value in settings

    :params string key:  lookup key
    '''
    return settings.get(key, None)
