import logging
import os

from requests import api
from requests_toolbelt import MultipartEncoder
from edcore.exceptions import RemoteCopyError
from hpz_client.frs.config import Config, get_setting
import json
import traceback

__author__ = 'ablum'

log = logging.getLogger('smarter')


def __create_stream(file_path, file):
    return {'file': (file_path, file, 'application/octet-stream')}


def __create_mail(mail_from, subject, content):
    fields = {}
    if mail_from is not None and content is not None:
        data = {'from': mail_from, 'subject': subject, 'content': content}
        fields = {'mail': json.dumps(data)}
    return fields


def __create_MultipartEncoder(fields):
    return MultipartEncoder(fields=fields)


def http_file_upload(file_path, registration_id, email_from=None, email_subject=None, email_content=None):
    upload_url = get_setting(Config.HPZ_FILE_UPLOAD_BASE_URL)
    if email_content is None:
        upload_url = upload_url + '/default/' + registration_id
        mail = {}
    else:
        upload_url = upload_url + '/custom/' + registration_id
        mail = __create_mail(email_from, email_subject, email_content)
    verify_certificate = not get_setting(Config.HPZ_IGNORE_CERTIFICATE)
    response = None
    headers = {}
    if file_path is not None:
        with open(file_path, 'rb') as f:
            stream = __create_stream(file_path, f)
            if mail:
                mail.update(stream)
            else:
                mail = stream
            headers = {'File-Name': os.path.basename(file_path)}
            multipartEncorder = __create_MultipartEncoder(mail)
            headers['Content-Type'] = multipartEncorder.content_type
            try:
                response = api.post(upload_url, data=multipartEncorder, headers=headers, verify=verify_certificate)
                log.info("File uploaded to %s with status code %d" % (upload_url, response.status_code))
            except ConnectionError as e:
                raise RemoteCopyError(msg=str(e))
            except TypeError as e:
                # Known Bug in Python 3.3.0.  We need to swallow the exception here
                log.warning("Caught Known Exception: " + str(e))
    else:
        try:
            response = api.post(upload_url, data=mail, verify=verify_certificate)
            log.info("File uploaded to %s with status code %d" % (upload_url, response.status_code))
        except ConnectionError as e:
            raise RemoteCopyError(msg=str(e))
        except TypeError as e:
            # Known Bug in Python 3.3.0.  We need to swallow the exception here
            log.warning("Caught Known Exception: " + str(e))
    return response.status_code if response else None
