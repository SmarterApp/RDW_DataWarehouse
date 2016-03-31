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
