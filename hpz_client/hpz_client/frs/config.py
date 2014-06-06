__author__ = 'tshewchuk'
"""
This module stores the relevant information needed by the HPZ Client functions.
"""


class Config:
    HPZ_FILE_REGISTRATION_URL = 'hpz.file_registration_url'
    HPZ_FILE_UPLOAD_BASE_URL = 'hpz.file_upload_base_url'


_DEFAULTS = [(Config.HPZ_FILE_REGISTRATION_URL, str, 'http://localhost/registration'),
             (Config.HPZ_FILE_UPLOAD_BASE_URL, str, 'http://localhost/files')]

# HPZ Client-specific settings, filled from application's ini settings.
_settings = {}


def initialize(config):
    global _settings
    for item in _DEFAULTS:
        key = item[0]
        to_type = item[1]
        default = item[2]
        _settings[key] = to_type(config.get(key, default))


def get_setting(key, default_value=None):
    return _settings.get(key, default_value)
