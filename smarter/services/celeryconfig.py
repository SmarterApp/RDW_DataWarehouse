'''
Created on May 9, 2013

@author: tosako
'''
from celery.app.base import Celery

celery = Celery()


def setup_celery(celery_config):
    celery.config_from_object(celery_config)

def load_config(settings, prefix="celery"):
    """ Loads celery configuration from setting dict.
        Any value whose corresponding key starts with prefix and followed by a period 
        is considered as celery configuration.
        Configuration key will be stored in uppercase as celery's convention.
    """
    celery_config = {}
    prefix = prefix + "."
    # get config values
    for key in settings:
        if key.startswith(prefix):
            celery_key = key[len(prefix):].upper()
            celery_config[celery_key] = settings[key]
    return celery_config
