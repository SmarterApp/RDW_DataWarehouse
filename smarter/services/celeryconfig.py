'''
Created on May 9, 2013

@author: tosako
'''
from celery.app.base import Celery

celery = Celery()


def start_celery(settings):
    # get config values
    broker_url = settings.get('celery.broker_url')
    always_eager = settings.get('celery.celery_always_eager')
    # set up config as a dict
    celery_config = {'BROKER_URL': broker_url,
                     'CELERY_ALWAYS_EAGER': always_eager}
    celery.config_from_object(celery_config)
