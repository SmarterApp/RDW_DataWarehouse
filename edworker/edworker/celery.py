'''
Created on May 14, 2013

@author: dip
'''
import os
from celery import Celery
import configparser
from edworker.celeryconfig import get_config


def setup_celery(celery, settings, prefix='celery'):
    '''
    Setup celery based on parameters defined in setting (ini file)

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    celery_config = get_config(settings, prefix)
    celery.config_from_object(celery_config)


def configure_celeryd(name, prefix='celery'):
    celery = Celery(name)
    # Read environment variable that is set in prod mode that stores path of smarter.ini
    prod_config = get_config_file()
    if prod_config:
        # This is the entry point for celeryd daemon
        print("Reading config for production mode")
        # Read from ini then pass the object here
        config = configparser.RawConfigParser()
        config.read(prod_config)
        conf = {}
        section_name = 'app:main'
        options = config.options(section_name)
        for option in options:
            conf[option] = config.get(section_name, option)
        if 'smarter.path' in conf:
            os.environ['PATH'] += os.pathsep + conf['smarter.path']
        setup_celery(celery, conf, prefix=prefix)
    return celery


def get_config_file():
    # Read environment variable that is set in prod mode that stores path of smarter.ini
    prod_config = os.environ.get("CELERY_PROD_CONFIG")
    file_name = prod_config if (prod_config is not None and os.path.exists(prod_config)) else None
    return file_name
