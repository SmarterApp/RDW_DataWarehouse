'''
Created on Nov 8, 2013

@author: dip
'''
from celery.utils import strtobool


class Config():
    JAIL_BASE_PATH = 'sftp.jail.base_path'
    PICKUP_HOME_BASE_PATH = 'pickup.home.base_path'
    MAX_RETRIES = 'extract.retries_allowed'
    RETRY_DELAY = 'extract.retry_delay'
    TIMEOUT = 'extract.timeout'
    GATEKEEPER = 'pickup.gatekeeper.'
    DISABLE_SFTP = 'extract.disable.sftp'       # When set to true, it'll copy to directory (for local testing)

# Keeps track of configuration related to edextract that is read off from ini
settings = {}


def setup_settings(config):
    # list of configurations that are specific to edextract
    list_of_config = [(Config.JAIL_BASE_PATH, str, '/sftp'),
                      (Config.PICKUP_HOME_BASE_PATH, str, '/pickup'),
                      (Config.MAX_RETRIES, int, 1),
                      (Config.RETRY_DELAY, int, 60),
                      (Config.TIMEOUT, int, 20),
                      (Config.DISABLE_SFTP, strtobool, 'False')
                      ]

    global settings
    for item in list_of_config:
        key = item[0]
        to_type = item[1]
        default = item[2]
        settings[key] = to_type(config.get(key, default))

    gatekeeper = {}
    for key in config.keys():
        if key.startswith(Config.GATEKEEPER):
            tenant = key[len(Config.GATEKEEPER):]
            gatekeeper[tenant] = config[key]
    settings[Config.GATEKEEPER] = gatekeeper


def get_gatekeeper(tenant):
    return settings[Config.GATEKEEPER].get(tenant)
