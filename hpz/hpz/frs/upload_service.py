"""
This module describes the file upload endpoint for HPZ.
"""
from hpz.frs.mail import sendmail
from hpz.database.constants import HPZ
import pkg_resources
import json
from pyramid.httpexceptions import HTTPNotFound
__author__ = 'ablum,'
__author__ = 'tshewchuk'

import os
import shutil
import logging

from pyramid.response import Response
from pyramid.view import view_config

from hpz.database.file_registry import FileRegistry
from hpz.frs.decorators import validate_request_info
from urllib.parse import urljoin
from jinja2 import Template


logger = logging.getLogger(__name__)
FILE_NAME_HEADER = 'File-Name'
FILE_BODY_ATTRIBUTE = 'file'


@view_config(route_name='files_with_custom_notification', renderer='json', request_method='POST')
def file_upload_service_with_custom_notification(context, request):
    registration_id = request.matchdict['registration_id']
    if FileRegistry.is_file_registered(registration_id):
        custom_mail = request.POST['mail']
        mail_json = json.loads(custom_mail)
        mail_from = mail_json.get('from')
        mail_return_path = mail_from
        mail_subject = mail_json.get('subject')
        mail_content = mail_json.get('content')
        __file_upload_service(request, mail_from, mail_return_path, mail_subject, mail_content)


@view_config(route_name='files_with_default_notification', renderer='json', request_method='POST')
@validate_request_info('headers', FILE_NAME_HEADER)
@validate_request_info('POST', FILE_BODY_ATTRIBUTE)
def file_upload_service_with_default_notification(context, request):
    registration_id = request.matchdict['registration_id']
    if FileRegistry.is_file_registered(registration_id):
        try:
            template_filename = os.path.join(pkg_resources.resource_filename('hpz', 'templates'), "reports_available.j2")
            mail_content = None
            with open(template_filename) as fh:
                base_url = request.registry.settings.get('hpz.frs.download_base_url')
                hpz_web_url = urljoin(base_url, '/download/' + registration_id)
                template_text = fh.read()
                template = Template(template_text)
                mail_content = template.render({"hpz_url": hpz_web_url})
            mail_from = request.registry.settings.get('hpz.mail.sender')
            mail_return_path = request.registry.settings.get('hpz.mail.return_path', mail_from)
            mail_subject = request.registry.settings.get('hpz.mail.subject')
            __file_upload_service(request, mail_from, mail_return_path, mail_subject, mail_content)
            return Response()
        except Exception as e:
            pass
    return HTTPNotFound()


def __file_upload_service(request, mail_from, mail_return_path, mail_subject, mail_content):
    try:
        registration_id = request.matchdict['registration_id']
        file_name = request.headers.get(FILE_NAME_HEADER)
        if file_name is not None:
            base_upload_path = request.registry.settings['hpz.frs.upload_base_path']
            file_size_limit = int(request.registry.settings['hpz.frs.file_size_limit'])
            file_pathname = os.path.join(base_upload_path, registration_id)
            input_file = request.POST['file'].file
            with open(file_pathname, mode='wb') as output_file:
                shutil.copyfileobj(input_file, output_file)
            if os.path.getsize(file_pathname) > file_size_limit:
                logger.warning('File %s exceeds recommended size limit', file_pathname)
            FileRegistry.update_registration(registration_id, file_pathname, file_name)
            logger.info('File %s was successfully uploaded', file_pathname)
        mail_server = request.registry.settings.get('hpz.mail.server')
        mail_port = request.registry.settings.get('hpz.mail.port', 465)
        if type(mail_port) is str:
            mail_port = int(mail_port)

        aws_mail_username = request.registry.settings.get('hpz.mail.smtp_username')
        aws_mail_password = request.registry.settings.get('hpz.mail.smtp_password')

        if mail_server is not None and mail_server != 'None':
            registration = FileRegistry.get_registration_info(registration_id)
            user_id = registration[HPZ.EMAIL]
            email = True
            try:
                email = sendmail(mail_server, mail_port, mail_from, user_id, mail_return_path, mail_subject, aws_mail_username, aws_mail_password, mail_content)
            except:
                email = False
            if email is False:
                logger.error('failed to sent email to ' + user_id)
    except IOError as e:
        logger.error('Cannot complete file copying due to: %s' % str(e))
        raise
