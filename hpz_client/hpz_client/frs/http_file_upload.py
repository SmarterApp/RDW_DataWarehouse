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
