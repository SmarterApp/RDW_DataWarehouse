import logging
import os

from pyramid.threadlocal import get_current_registry

from requests import api
from requests_toolbelt import MultipartEncoder
from edcore.exceptions import RemoteCopyError

__author__ = 'ablum'

log = logging.getLogger('smarter')


def __create_stream(file_path, file):
    return MultipartEncoder(fields={'file': (file_path, file, 'application/octet-stream')})


def http_file_upload(file_path, registration_id):
    log.info('############## http_file_upload: registration_id = ' + registration_id)
    upload_url = get_current_registry().settings.get('hpz.file_upload_base_url') + '/' + registration_id
    log.info('############## http_file_upload: upload_url = ' + upload_url)

    with open(file_path, 'rb') as f:
        stream = __create_stream(file_path, f)
        headers = {'Content-Type': stream.content_type, 'File-Name': os.path.basename(file_path)}

        try:
            log.info('############## http_file_upload: pre-api.post')
            response = api.post(upload_url, data=stream, headers=headers)
            log.info('############## http_file_upload: post-api.post')

        except ConnectionError as e:
            raise RemoteCopyError(msg=str(e))

        log.info("File uploaded to %s with status code %d" % (upload_url, response.status_code))

        return response.status_code
