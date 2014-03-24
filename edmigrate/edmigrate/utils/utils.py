'''
Created on Mar 17, 2014

@author: tosako
'''
from edmigrate.settings.config import get_setting, Config


def get_broker_url():
    url = "memory://"
    celery_always_eager = get_setting(Config.EAGER_MODE, False)
    if not celery_always_eager:
        url = get_setting(Config.BROKER_URL, url)
    return url


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]
