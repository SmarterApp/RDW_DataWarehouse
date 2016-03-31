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
This module contains the functionality for registering extract files with the HPZ.
"""

import json
from requests import put
from hpz_client.frs.config import Config, get_setting


def register_file(user_id, email):
    registration_url = get_setting(Config.HPZ_FILE_REGISTRATION_URL)
    registration_body = {'uid': user_id, 'email': email}
    verify_certificate = not get_setting(Config.HPZ_IGNORE_CERTIFICATE)

    response = put(registration_url, json.dumps(registration_body), verify=verify_certificate)
    response_json = response.json()
    registration_id = response_json['registration_id']
    download_url = response_json['url']
    web_download_url = response_json['web_url']

    return registration_id, download_url, web_download_url
