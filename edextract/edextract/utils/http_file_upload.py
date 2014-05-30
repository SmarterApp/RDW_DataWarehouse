import logging
from requests.api import post
from requests_toolbelt import MultipartEncoder

__author__ = 'ablum'

log = logging.getLogger('smarter')


def __create_stream(file_name):
    return MultipartEncoder(fields={'file': (file_name, open(file_name, 'rb'), 'application/octet-stream')})


def http_file_upload(file_name, upload_url):

    stream = __create_stream(file_name)
    headers = {'Content-Type': stream.content_type, 'File-Name': file_name}

    response = post(upload_url, data=stream, headers=headers)
    log.info("File uploaded to %s with status code %d" % (upload_url, response.status))
