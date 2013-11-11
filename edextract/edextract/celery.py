'''
Created on Nov 4, 2013

@author: dip
'''
from edworker.celery import setup_celery as setup, configure_celeryd,\
    get_config_file
from edextract.status.status import setup_db_connection
from edextract.settings.config import setup_settings

PREFIX = 'extract.celery'


def setup_celery(settings, prefix=PREFIX):
    '''
    Setup celery based on parameters defined in setting (ini file).
    This calls by client application when dictionary of settings is given

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    setup(celery, settings, prefix)
    setup_settings(settings)


# Create an instance of celery, check if it's for prod celeryd mode and configure it for prod mode if so
celery = configure_celeryd(PREFIX, prefix=PREFIX)
prod_config = get_config_file()
if prod_config:
    # We should only need to setup db connection in prod mode
    setup_db_connection(prod_config)
    setup_settings(prod_config)
