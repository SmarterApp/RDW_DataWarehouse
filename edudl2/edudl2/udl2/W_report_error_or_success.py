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

from __future__ import absolute_import
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.message_keys import EMAIL


logger = get_task_logger(__name__)


@celery.task(name='udl2.W_report_error_or_success.task')
def task(msg):
    '''
    Celery task to report error or success. the message expects to contain
    'email_address'
    '''
    logger.info(task.name)
    logger.info('Report Error or Success Dummy')
    assert msg[EMAIL]

    #TODO: report

    return msg
