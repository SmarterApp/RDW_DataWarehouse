'''
Created on May 9, 2013

@author: tosako
'''
from celery.app.base import Celery

celery = Celery()


def setup_celery(settings):
    celery_config = {}
    # get config values
    for key in settings:
        if key.startswith('celery'):
            celery_key = key[len('celery.'):].upper()
            celery_config[celery_key] = settings[key]
    celery.config_from_object(celery_config)

def get_config(setting, prefix="celery"):
    pass