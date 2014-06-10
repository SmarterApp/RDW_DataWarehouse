__author__ = 'tshewchuk'
"""
This module contains the functionality for registering extract files with the HPZ.
"""

import json
from requests import put
from hpz_client.frs.config import Config, get_setting


def register_file(user_id):
    registration_url = get_setting(Config.HPZ_FILE_REGISTRATION_URL)
    registration_body = {'uid': user_id}
    verify_certificate = not get_setting(Config.HPZ_IGNORE_CERTIFICATE)

    response = put(registration_url, json.dumps(registration_body), verify=verify_certificate)
    response_json = response.json()
    registration_id = response_json['registration_id']
    download_url = response_json['url']

    return registration_id, download_url
