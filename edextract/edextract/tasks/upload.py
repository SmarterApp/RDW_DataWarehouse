import logging
from edextract.celery import celery
from edextract.exceptions import ExtractionError
from edextract.settings.config import get_setting, Config
from edextract.status.constants import Constants
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.utils.http_file_upload import http_file_upload

__author__ = 'ablum'
log = logging.getLogger('edextract')
MAX_RETRY = get_setting(Config.MAX_RETRIES, 1)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY, 60)


@celery.task(name="tasks.extract.http_upload",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def upload(request_id, src_file_name, http_info):
    '''
    Remotely copies a source file to a remote machine
    '''
    task_info = {Constants.TASK_ID: upload.request.id,
                 Constants.CELERY_TASK_ID: upload.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPYING})

        http_file_upload(src_file_name, http_info['url'])

        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPIED})
    except ConnectionError as e:
        log.error("Connection refused. File was not able to be uploaded. " + str(e))
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: 'http upload has failed: ' + str(e)})

        try:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            raise ExtractionError(str(e))
        except ExtractionError as exc:
            # this could be caused by network hiccup
            raise upload.retry(args=[request_id, src_file_name, http_info], exc=exc)

    except Exception as e:
        raise ExtractionError(str(e))
