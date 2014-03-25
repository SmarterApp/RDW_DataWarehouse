__author__ = 'sravi'
from edmigrate.utils.constants import Constants
import ast
import logging
from logging.handlers import SysLogHandler


class Config():
    MASTER_SCHEDULER_HOUR = 'migrate.master_scheduler.hour'
    MASTER_SCHEDULER_MIN = 'migrate.master_scheduler.min'
    MAX_RETRIES = 'migrate.retries_allowed'
    RETRY_DELAY = 'migrate.retry_delay'
    TIMEOUT = 'migrate.timeout'
    BROADCAST_QUEUE = 'migrate.broadcast.queue'
    LAG_TOLERENCE_IN_BYTES = 'migrate.lag_tolerence_in_bytes'
    PGPOOL_HOSTNAME = 'migrate.pgpool.hostname'
    MASTER_HOSTNAME = 'migrate.master.hostname'
    IPTABLES_CHAIN = 'migrate.iptables.chain'
    IPTABLES_SUDO = 'migrate.iptables.sudo'
    IPTABLES_COMMAND = 'migrate.iptables.command'
    DEFAULT_ROUTUNG_KEY = 'migrate.celery.CELERY_DEFAULT_ROUTING_KEY'
    DEFAULT_ROUTUNG_QUEUE = 'migrate.celery.CELERY_DEFAULT_ROUTING_QUEUE'
    BROKER_URL = 'migrate.celery.BROKER_URL'
    EAGER_MODE = 'migrate.celery.celery_always_eager'
    SYSLOG_ADDRESS = 'migrate.syslog.address'


# list of configurations that are specific to edmigrate
LIST_OF_CONFIG = [(Config.MASTER_SCHEDULER_HOUR, int, 0),
                  (Config.MASTER_SCHEDULER_MIN, int, 1),
                  (Config.MAX_RETRIES, int, 10),
                  (Config.RETRY_DELAY, int, 60),
                  (Config.TIMEOUT, int, 20),
                  (Config.BROADCAST_QUEUE, str, None),
                  (Config.LAG_TOLERENCE_IN_BYTES, int, 10),
                  (Config.PGPOOL_HOSTNAME, str, None),
                  (Config.DEFAULT_ROUTUNG_KEY, str, Constants.WORKER_NAME),
                  (Config.DEFAULT_ROUTUNG_QUEUE, str, Constants.CONDUCTOR_QUEUE),
                  (Config.BROKER_URL, str, 'memory://'),
                  (Config.EAGER_MODE, bool, False),
                  (Config.MASTER_HOSTNAME, str, Constants.LOCALHOST),
                  (Config.IPTABLES_CHAIN, str, Constants.IPTABLES_CHAIN),
                  (Config.IPTABLES_COMMAND, str, Constants.IPTABLES_COMMAND),
                  (Config.IPTABLES_SUDO, str, Constants.IPTABLES_SUDO),
                  (Config.SYSLOG_ADDRESS, str, None)]


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


def setup_syslog(settings):
    logger = logging.getLogger(Constants.WORKER_NAME)
    syslog_address = get_setting(Config.SYSLOG_ADDRESS, None)
    # parse the address settings
    if type(syslog_address) == str:
        syslog_address = ast.literal_eval(syslog_address)
    # fails when syslog_address is not as tuple, str, or None. log error to user
    if type(syslog_address) not in [str, tuple, type(None)]:
        logger.error("{name} can't set up syslogger due to configuration error in format ".format(name=Constants.WORKER_NAME))

    if syslog_address is not None:
        # the input is not in right format
        if type(syslog_address) == tuple and len(syslog_address) not in [1, 2]:
            logger.error("{name} can't set up syslogger due to configuration errors in wrong tuple.".
                         format(name=Constants.WORKER_NAME))

        logger = logging.getLogger(Constants.WORKER_NAME)
        syslog_handler = SysLogHandler(address=syslog_address)
        syslog_handler.setLevel(logging.ERROR)
        logger.addHandler(syslog_handler)
