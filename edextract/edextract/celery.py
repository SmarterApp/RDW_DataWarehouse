'''
Created on Nov 4, 2013

@author: dip
'''
from edworker.celery import setup_celery as setup, configure_celeryd

PREFIX = 'extract.celery'


def setup_celery(settings, prefix=PREFIX):
    '''
    Setup celery based on parameters defined in setting (ini file).  
    This calls by client application when dictionary of settings is given

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    setup(celery, settings, prefix)

# Create an instance of celery, check if it's for prod celeryd mode and configure it for prod mode if so
celery = configure_celeryd('extract.celery', prefix=PREFIX)
