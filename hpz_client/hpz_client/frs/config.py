# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'tshewchuk'
"""
This module stores the relevant information needed by the HPZ Client functions.
"""


class Config:
    HPZ_FILE_REGISTRATION_URL = 'hpz.file_registration_url'
    HPZ_FILE_UPLOAD_BASE_URL = 'hpz.file_upload_base_url'
    HPZ_IGNORE_CERTIFICATE = 'hpz.ignore_certificate'


_DEFAULTS = [(Config.HPZ_FILE_REGISTRATION_URL, str, 'http://localhost/registration'),
             (Config.HPZ_FILE_UPLOAD_BASE_URL, str, 'http://localhost/files'),
             (Config.HPZ_IGNORE_CERTIFICATE, bool, False)]

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
