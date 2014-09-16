'''
Created on Sep 9, 2014

@author: tosako
'''
from email.mime.text import MIMEText
import smtplib
import json


def send_notification_email(mail_server, msg_from, msg_to, subject, message):
    '''
    sending e-mail
    :param mail_server: mail server host name
    :param msg_from: sender's e-mail address
    :param msg_to: receiver's e-mail address
    :param subject: subject
    :param message: message
    '''
    msg = MIMEText(message if type(message) is str else json.dumps(message))
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    with smtplib.SMTP(mail_server) as mail:
        mail.send_message(msg)
        mail.quit()
