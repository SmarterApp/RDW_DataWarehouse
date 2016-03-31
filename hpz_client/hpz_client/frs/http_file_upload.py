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

import logging
import os

from requests import api
from requests_toolbelt import MultipartEncoder
from edcore.exceptions import RemoteCopyError
from hpz_client.frs.config import Config, get_setting

__author__ = 'ablum'

log = logging.getLogger('smarter')


def __create_stream(file_path, file):
    return MultipartEncoder(fields={'file': (file_path, file, 'application/octet-stream')})


def http_file_upload(file_path, registration_id):
    upload_url = get_setting(Config.HPZ_FILE_UPLOAD_BASE_URL) + '/' + registration_id
    verify_certificate = not get_setting(Config.HPZ_IGNORE_CERTIFICATE)
    response = None
    with open(file_path, 'rb') as f:
        stream = __create_stream(file_path, f)
        headers = {'Content-Type': stream.content_type, 'File-Name': os.path.basename(file_path)}
        try:
            response = api.post(upload_url, data=stream, headers=headers, verify=verify_certificate)
            log.info("File uploaded to %s with status code %d" % (upload_url, response.status_code))
        except ConnectionError as e:
            raise RemoteCopyError(msg=str(e))
        except TypeError as e:
            # Known Bug in Python 3.3.0.  We need to swallow the exception here
            log.warning("Caught Known Exception: " + str(e))
        return response.status_code if response else None
