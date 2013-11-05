'''
Created on Nov 4, 2013

@author: dip
'''
from edworker.celery import setup_celery as setup, configure_celeryd,\
    get_config_file
from edextract.extract_status import setup_db_connection

# default timeout 20 seconds
TIMEOUT = 20
# default number of pdf generation retries
MAX_RETRIES = 1
# minimum file size of pdf generated
MINIMUM_FILE_SIZE = 80000
# delay in retry. Default to 5 seconds
RETRY_DELAY = 5

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
celery = configure_celeryd(PREFIX, prefix=PREFIX)
prod_config = get_config_file()
if prod_config:
    # We should only need to setup db connection in prod mode
    setup_db_connection(prod_config)
