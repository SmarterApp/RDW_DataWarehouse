'''
Created on May 14, 2013

@author: dip
'''
import os
from celery import Celery
import configparser
from services.celeryconfig import get_config


def setup_celery(settings, prefix='celery'):
    '''
    Setup celery based on parameters defined in setting (ini file)
    '''
    celery_config = get_config(settings, prefix)
    celery.config_from_object(celery_config)


celery = Celery('pdf_service')

# Read environment variable that is set in prod mode that stores path of smarter.ini
prod_config = os.environ.get("CELERY_PROD_CONFIG")

if prod_config:
    # This is the entry point for celeryd daemon
    print("Config for production mode")

    if os.path.exists(prod_config):
        # Read from ini then pass the object here
        config = configparser.RawConfigParser()
        config.read(prod_config)
        conf = {}
        section_name = 'app:main'
        options = config.options(section_name)
        for option in options:
            conf[option] = config.get(section_name, option)

        setup_celery(conf)
