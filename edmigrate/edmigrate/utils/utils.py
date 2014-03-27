'''
Created on Mar 17, 2014

@author: tosako
'''
from edmigrate.settings.config import Config, setup_settings, get_setting
from edworker.celery import get_config_file
import configparser


def read_ini(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config['app:main']


def get_broker_url(config=None):
    if config is None:
        config_file = get_config_file()
        if config_file is None:
            config = configparser.ConfigParser()
        else:
            config = read_ini(config_file)

    url = "memory://"

    try:
        celery_always_eager = config.getboolean(Config.EAGER_MODE, False)
    except:
        celery_always_eager = False

    if not celery_always_eager:
        try:
            url = config.get(Config.BROKER_URL, url)
        except:
            pass
    return url


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]
