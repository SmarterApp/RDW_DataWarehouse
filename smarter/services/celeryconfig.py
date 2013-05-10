'''
Created on May 9, 2013

@author: tosako
'''
from celery.app.base import Celery


celery = Celery()

def start_celery(celery_config):
    celery.config_from_object(celery_config)
