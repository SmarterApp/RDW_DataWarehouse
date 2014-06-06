__author__ = 'tshewchuk'
"""
This module stores the relevant information needed by the HPZ Client functions.
"""


class Config:
    HPZ_FILE_REGISTRATION_URL = 'hpz.file_registration_url'
    HPZ_FILE_UPLOAD_URL = 'hpz.file_upload_base_url'


_settings = {Config.HPZ_FILE_REGISTRATION_URL: 'http://localhost/registration',
             Config.HPZ_FILE_UPLOAD_URL: 'http://localhost/files'}


def initialize(config):
    global _settings
    _settings[Config.HPZ_FILE_REGISTRATION_URL] = config.get(Config.HPZ_FILE_REGISTRATION_URL)
    _settings[Config.HPZ_FILE_UPLOAD_URL] = config.get(Config.HPZ_FILE_UPLOAD_URL)


def get_setting(key):
    return _settings.get(key)
