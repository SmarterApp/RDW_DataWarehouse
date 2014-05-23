__author__ = 'tshewchuk'
"""
This module contains the functionality for registering and uploading extract files to the HPZ.
"""

import json
from pyramid.threadlocal import get_current_registry
from requests import put

DEFAULT_REG_BASE_URL = 'http://localhost'
DEFAULT_REG_ENDPOINT = '/registration'


def register_file(user_id):
    registration_url = get_current_registry().settings.get('hpz.base_url', DEFAULT_REG_BASE_URL) + \
        get_current_registry().settings.get('hpz.registration_endpoint', DEFAULT_REG_ENDPOINT)

    registration_body = {'uid': user_id}

    response = put(registration_url, json.dumps(registration_body))

    registration_id = response.json()['registration_id']
    download_url = response.json()['url']

    return registration_id, download_url
