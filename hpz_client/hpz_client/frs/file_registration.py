__author__ = 'tshewchuk'
"""
This module contains the functionality for registering extract files with the HPZ.
"""

import json
from pyramid.threadlocal import get_current_registry
from requests import put


def register_file(user_id):
    registration_url = get_current_registry().settings.get('hpz.file_registration_url')
    registration_body = {'uid': user_id}

    response = put(registration_url, json.dumps(registration_body))
    response_json = response.json()
    registration_id = response_json['registration_id']
    download_url = response_json['url']

    return registration_id, download_url
