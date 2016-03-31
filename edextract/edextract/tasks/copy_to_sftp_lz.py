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

__author__ = 'tshewchuk'
"""
This module contains the previous remote_copy task, renamed to copy_to_sftp_lz.
It's a placeholder for the no longer used remote_copy task which copied files to the sftp landing zone.
"""

from edextract.celery import celery
from edextract.settings.config import Config, get_setting
from edextract.status.constants import Constants
from edextract.status.status import ExtractStatus, insert_extract_stats
import edextract.utils.file_remote_copy
from edcore.exceptions import RemoteCopyError
from edextract.exceptions import ExtractionError
import logging

MAX_RETRY = get_setting(Config.MAX_RETRIES, 1)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY, 60)

log = logging.getLogger('edextract')


@celery.task(name="tasks.copy_to_sftp_lz.copy_to_sftp_lz",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def copy_to_sftp_lz(request_id, src_file_name, tenant, gatekeeper, sftp_info, timeout=1800):
    '''
    Remotely copies a source file to a remote machine
    '''
    task_info = {Constants.TASK_ID: copy_to_sftp_lz.request.id,
                 Constants.CELERY_TASK_ID: copy_to_sftp_lz.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPYING})
        edextract.utils.file_remote_copy.copy(src_file_name, sftp_info[0], tenant, gatekeeper, sftp_info[1], sftp_info[2], timeout=timeout)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPIED})
    except RemoteCopyError as e:
        log.error("Exception happened in remote copy to sftp lz. " + str(e))
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: 'remote copy to sftp lz has failed: ' + str(e)})
        try:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            raise ExtractionError(str(e))
        except ExtractionError as exc:
            # this could be caused by network hiccup
            raise copy_to_sftp_lz.retry(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info], kwargs={'timeout': timeout}, exc=exc)
    except Exception as e:
        raise ExtractionError(str(e))
