__author__ = 'sravi'


class Config():
    MASTER_SCHEDULER_HOUR = 'edload.master_scheduler.hour'
    MASTER_SCHEDULER_MIN = 'edload.master_scheduler.min'

# list of configurations that are specific to edextract
LIST_OF_CONFIG = [(Config.MASTER_SCHEDULER_HOUR, int, 0),
                  (Config.MASTER_SCHEDULER_MIN, int, 1)]

# Keeps track of configuration related to edload that is read off from ini
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


def get_setting(key, default_value=None):
    '''
    Given a key, look up value in settings

    :params string key:  lookup key
    '''
    return settings.get(key, default_value)
