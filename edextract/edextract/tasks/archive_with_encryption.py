__author__ = 'tshewchuk'
"""
This module contains the previous archive task, renamed to archive_with_encryption.
It's a placeholder for the no longer used archive task which included encryption.
"""

from edextract.settings.config import Config, get_setting
from edextract.celery import celery
from edextract.status.constants import Constants
from edextract.status.status import ExtractStatus, insert_extract_stats
from edcore.utils.data_archiver import encrypted_archive_files, GPGPublicKeyException
from edextract.exceptions import ExtractionError


MAX_RETRY = get_setting(Config.MAX_RETRIES, 1)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY, 60)


@celery.task(name="tasks.archive_with_encryption.archive_with_encryption", max_retries=MAX_RETRY, default_retry_delay=DEFAULT_RETRY_DELAY)
def archive_with_encryption(request_id, recipients, archive_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''

    retryable = False
    exception_thrown = False

    try:
        task_info = {Constants.TASK_ID: archive_with_encryption.request.id,
                     Constants.CELERY_TASK_ID: archive_with_encryption.request.id,
                     Constants.REQUEST_GUID: request_id}
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVING})

        gpg_binary_file = get_setting(Config.BINARYFILE)
        homedir = get_setting(Config.HOMEDIR)
        keyserver = get_setting(Config.KEYSERVER)
        encrypted_archive_files(directory, recipients, archive_file_name, homedir=homedir, keyserver=keyserver, gpgbinary=gpg_binary_file)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVED})
    except GPGPublicKeyException as e:
        # recoverable exception
        retryable = True
        exception_thrown = True
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
    except Exception as e:
        # unrecoverable exception
        exception_thrown = True
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})

    if exception_thrown:
        if retryable:
            try:
                # this looks funny to you, but this is just a working around solution for celery bug
                # since exc option is not really working for retry.
                raise ExtractionError()
            except ExtractionError as exc:
                raise archive_with_encryption.retry(args=[request_id, recipients, archive_file_name, directory], exc=exc)
        else:
            raise ExtractionError()
