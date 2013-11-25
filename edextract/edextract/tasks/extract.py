'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''
import csv
import logging
from edextract.celery import celery
from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.status.status import ExtractStatus,\
    insert_extract_stats
from edextract.status.constants import Constants
from edextract.utils.file_encryptor import FileEncryptor
from edextract.settings.config import Config, get_setting
from edextract.utils.file_utils import prepare_path
from edextract.utils.file_archiver import archive_files
from celery.canvas import group, chain
from edextract.utils.file_remote_copy import copy
from edextract.exceptions import RemoteCopyError


log = logging.getLogger('edextract')


@celery.task(name='task.extract.start_extract',
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def start_extract(tenant, request_id, public_key_id, archive_file_name, directory_to_archive, gatekeeper_id, pickup_zone_info, tasks):
    '''
    entry point to start an extract request for one or more extract tasks
    it groups the generation of csv into a celery task group and then chains it to the next task to archive the files into one zip
    '''
    generate_tasks = group(generate.subtask(args=[tenant, request_id, public_key_id, task['task_id'], task['query'], task['file_name']], queue='extract', immutable=True) for task in tasks)
    workflow = chain(generate_tasks,
                     archive.subtask(args=[request_id, archive_file_name, directory_to_archive], queue='extract', immutable=True),
                     remote_copy.subtask(args=[request_id, archive_file_name, tenant, gatekeeper_id, pickup_zone_info], queue='extract', immutable=True))
    workflow.apply_async()


@celery.task(name="tasks.extract.generate",
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def generate(tenant, request_id, public_key_id, task_id, query, output_file):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param tenant: tenant of the user
    :param query: extraction query to dump data
    :param params: request extraction input parameters
    :param output_uri: output file uri
    :param batch_id: batch_id for tracking
    '''
    log.info('execute tasks.extract.generate for task ' + task_id)
    try:
        task_info = {Constants.TASK_ID: task_id,
                     Constants.CELERY_TASK_ID: generate.request.id,
                     Constants.REQUEST_GUID: request_id}

        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTING})
        if tenant is None:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED_NO_TENANT})
            return False
        prepare_path(output_file)
        gpg_binary_file = get_setting(Config.BINARYFILE)
        homedir = get_setting(Config.HOMEDIR)
        with EdCoreDBConnection(tenant) as connection, FileEncryptor(output_file, public_key_id, homedir=homedir, binaryfile=gpg_binary_file) as csvfile:
            results = connection.get_streaming_result(query)  # this result is a generator
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            header = []
            for result in results:
                if len(header) is 0:
                    header = list(result.keys())
                    csvwriter.writerow(header)
                row = list(result.values())
                csvwriter.writerow(row)
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})
            return True
    except Exception as e:
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: e})
        return False


@celery.task(name="tasks.extract.archive",
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def archive(request_id, zip_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''
    task_info = {Constants.TASK_ID: archive.request.id,
                 Constants.CELERY_TASK_ID: archive.request.id,
                 Constants.REQUEST_GUID: request_id}
    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVING})
    prepare_path(zip_file_name)
    archive_files(zip_file_name, directory)
    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVED})


@celery.task(name="tasks.extract.remote_copy",
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def remote_copy(request_id, src_file_name, tenant, gatekeeper, sftp_info):
    task_info = {Constants.TASK_ID: remote_copy.request.id,
                 Constants.CELERY_TASK_ID: remote_copy.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPYING})
        rtn_code = copy(src_file_name, sftp_info[0], tenant, gatekeeper, sftp_info[1], sftp_info[2])
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPIED})
    except RemoteCopyError as e:
        log.error("Exception happened in remote copy. " + e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: 'remote copy has failed: ' + e})
    return rtn_code
