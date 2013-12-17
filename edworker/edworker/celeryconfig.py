'''
Created on May 9, 2013

@author: tosako
'''
from celery.app import defaults
import ast
from celery.utils import strtobool


def get_celeryconfig(settings, prefix='celery'):
    '''
    Returns celery configuration from setting dict.
    Any value whose corresponding key starts with prefix and followed by a period
    is considered as celery configuration.
    Configuration key will be stored in uppercase as celery's convention.

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    # load celery config
    celery_config = {}
    prefix = prefix + "."
    # get config values
    for key in settings:
        if key.startswith(prefix):
            celery_key = key[len(prefix):].upper()
            celery_config[celery_key] = settings[key]
    return convert_to_celery_options(celery_config)


def get_config(settings, prefix='celery'):
    '''
    Sets timeout for subprocess call in task and return Celery config

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    # load celery config
    celery_config = get_celeryconfig(settings, prefix)
    return celery_config


def convert_to_celery_options(config):
    '''
    Converts string representation of configuration to its expected data type

    :param config:  dict of configurations
    '''
    type_map = {'any': ast.literal_eval,
                'int': int,
                'string': str,
                'bool': strtobool,
                'float': float,
                'dict': ast.literal_eval,
                'tuple': ast.literal_eval,
                'list': ast.literal_eval
                }

    mapping = {}

    # Read from celery.app.defaults to get the expected data type for each configurable property
    for (key, value) in defaults.flatten(defaults.NAMESPACES):
        __type = type_map[value.type]
        if __type:
            mapping[key] = __type

    # For each config that need to configure, cast/convert to the expected data type
    for (key, value) in config.items():
        # EJ, BROKER_USE_SSL is not really bool. it is allowed to be a dict to hold cert information.
        # because we want our celery worker to share same configuration file as smarter. we need to make it parsable
        # so celery worker can use it
        # see
        # http://stackoverflow.com/questions/16406498/is-there-a-way-to-validate-the-brokers-ssl-certificate-in-django-celery
        # for BROKER_USE_SSL
        if mapping[key] and key != 'BROKER_USE_SSL':
            config[key] = mapping[key](value)
        else:
            config[key] = ast.literal_eval(value)
    return config
