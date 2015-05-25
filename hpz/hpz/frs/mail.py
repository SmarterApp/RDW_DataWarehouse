'''
Created on May 5, 2015

@author: tosako
'''
import os
import pkg_resources
from jinja2 import Template
from email.mime.text import MIMEText
import smtplib


def sendmail(mail_server, mail_port, mail_from, mail_to, mail_return_path, mail_subject, hpz_web_url, aws_mail_username, aws_mail_password):
    if mail_server is not None and mail_server != 'None':
        template_filename = os.path.join(pkg_resources.resource_filename('hpz', 'templates'), "reports_available.j2")
        with open(template_filename) as fh:
            template_text = fh.read()

            template = Template(template_text)
            email_text = template.render({"hpz_url": hpz_web_url})
            message = MIMEText(email_text)
            message["Subject"] = mail_subject
            message["From"] = mail_from
            message["Return-Path"] = mail_from if mail_return_path is None else mail_return_path
            message["To"] = mail_to

            with smtplib.SMTP_SSL(mail_server, mail_port) as mail:
                mail.login(aws_mail_username, aws_mail_password)
                mail.send_message(message)
                mail.quit()
                return True
    return False
