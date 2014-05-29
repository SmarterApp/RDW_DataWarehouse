__author__ = 'tshewchuk'
"""
This module contains the functionality for registering extract files with the HPZ.
"""

import json
from pyramid.threadlocal import get_current_registry
from requests import put
from requests.exceptions import ConnectionError
from simplejson.scanner import JSONDecodeError


def register_file(user_id):
    registration_url = get_current_registry().settings.get('hpz.file_registration_url')
    registration_body = {'uid': user_id}

    try:
        response = put(registration_url, json.dumps(registration_body))
        response_json = response.json()
        registration_id = response_json['registration_id']
        download_url = response_json['url']
    except (ConnectionError, JSONDecodeError):
        registration_id = ''
        download_url = ''

    return registration_id, download_url
