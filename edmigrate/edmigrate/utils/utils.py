'''
Created on Mar 17, 2014

@author: tosako
'''
from edmigrate.settings.config import Config, get_setting


def get_broker_url():
    url = "memory://"
    celery_always_eager = get_setting(Config.EAGER_MODE, False)
    if not celery_always_eager:
        url = get_setting(Config.BROKER_URL, url)
    return url
