'''
Created on May 9, 2013

@author: tosako
'''
from celery.app import defaults
import ast
from celery.utils import strtobool


# default timeout 20 seconds
TIMEOUT = 20


def load_celeryconfig(settings, prefix='celery'):
    '''
    Loads celery configuration from setting dict.
    Any value whose corresponding key starts with prefix and followed by a period
    is considered as celery configuration.
    Configuration key will be stored in uppercase as celery's convention.
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


def load_config(settings, prefix='celery'):
    '''
    Sets timeout for subprocess call in task and return Celery config
    '''
    global TIMEOUT
    TIMEOUT = settings.get('pdf.generate.timeout', TIMEOUT)
    # load celery config
    celery_config = load_celeryconfig(settings, prefix)
    return celery_config


def convert_to_celery_options(config):
    '''
    Converts string representation of configuration to its expected data type
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

    # Read from celery.app.defaults to get the expected data type for each configuarable property
    for (key, value) in defaults.flatten(defaults.NAMESPACES):
        __type = type_map[value.type]
        if __type:
            mapping[key] = __type

    # For each config that need to configure, cast/convert to the expected data type
    for (key, value) in config.items():
        if mapping[key]:
            config[key] = mapping[key](value)
    return config
