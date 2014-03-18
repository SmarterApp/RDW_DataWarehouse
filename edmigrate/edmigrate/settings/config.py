__author__ = 'sravi'


class Config():
    MASTER_SCHEDULER_HOUR = 'migrate.master_scheduler.hour'
    MASTER_SCHEDULER_MIN = 'migrate.master_scheduler.min'
    MAX_RETRIES = 'migrate.retries_allowed'
    RETRY_DELAY = 'migrate.retry_delay'
    TIMEOUT = 'migrate.timeout'
    BROADCAST_QUEUE = 'migrate.broadcast.queue'
    LAG_TOLERENCE_IN_BYTES = 'migrate.lag_tolerence_in_bytes'
    PGPOOL_HOSTNAME = 'migrate.pgpool.hostname'
    DEFAULT_ROUTUNG_KEY = 'migrate.celery.CELERY_DEFAULT_ROUTING_KEY'
    DEFAULT_ROUTUNG_QUEUE = 'migrate.celery.CELERY_DEFAULT_ROUTING_QUEUE'
    BROKER_URL = 'migrate.celery.BROKER_URL'


# list of configurations that are specific to edmigrate
LIST_OF_CONFIG = [(Config.MASTER_SCHEDULER_HOUR, int, 0),
                  (Config.MASTER_SCHEDULER_MIN, int, 1),
                  (Config.MAX_RETRIES, int, 10),
                  (Config.RETRY_DELAY, int, 60),
                  (Config.TIMEOUT, int, 20),
                  (Config.BROADCAST_QUEUE, str, None),
                  (Config.LAG_TOLERENCE_IN_BYTES, int, 10),
                  (Config.PGPOOL_HOSTNAME, str, None),
                  (Config.DEFAULT_ROUTUNG_KEY, str, 'edmigrate'),
                  (Config.DEFAULT_ROUTUNG_QUEUE, str, 'edmigrate_master'),
                  (Config.BROKER_URL, str, 'memory://')]


# Keeps track of configuration related to edmigrate that is read off from ini
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
