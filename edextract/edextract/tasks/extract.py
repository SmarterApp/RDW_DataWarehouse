'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''
import csv
import logging
from edextract.celery import celery
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.utils.utils import multi_delete
from edextract.status.status import update_extract_stats, ExtractStatus
from edextract.status.constants import Constants
from edextract.utils.file_encryptor import FileEncryptor
from datetime import datetime
from edextract.settings.config import Config, get_setting
from edextract.utils.file_utils import prepare_path
from edextract.utils.file_archiver import archive_files
from celery.canvas import group, chain
from edextract.utils.file_remote_copy import copy


log = logging.getLogger('edextract')


@celery.task(name='task.extract.start_extract',
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def start_extract(tenant, request_id, public_key_id, archive_file_name, directory_to_archive, tasks):
    '''
    entry point to start an extract request for one or more extract tasks
    it groups the generation of csv into a celery task group and then chains it to the next task to archive the files into one zip
    '''
    generate_tasks = group(generate.si(tenant, request_id, public_key_id, task['task_id'], task['query'], task['file_name']) for task in tasks)
    workflow = chain(generate_tasks,
                     archive.si(archive_file_name, directory_to_archive),
                     #remote_copy.si(archive_file_name, target_host_name, tenant, gatekeeper, sftp_user, private_key_path)
                     )
    workflow.apply_async(queue='extract')


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
    start_time = datetime.now()
    log.info('execute tasks.extract.generate for task ' + task_id)
    try:
        update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.EXTRACTING,
                                       Constants.EXTRACT_START: start_time,
                                       Constants.CELERY_TASK_ID: generate.request.id})
        if tenant is None:
            update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.NO_TENANT, Constants.EXTRACT_END: datetime.now()})
            return False
        prepare_path(output_file)
        gpg_binary_file = get_setting(Config.BINARYFILE)
        homedir = get_setting(Config.HOMEDIR)
        with EdCoreDBConnection(tenant) as connection, FileEncryptor(output_file, public_key_id, homedir=homedir, binaryfile=gpg_binary_file) as csvfile:
            results = connection.get_streaming_result(query)  # this result is a generator
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            header = []
            for result in results:
                # remove teacher names from results
                result = multi_delete(result, ['teacher_first_name', 'teacher_middle_name', 'teacher_last_name'])
                if len(header) is 0:
                    header = list(result.keys())
                    csvwriter.writerow(header)
                row = list(result.values())
                csvwriter.writerow(row)
            update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.EXTRACTED,
                                           Constants.EXTRACT_END: datetime.now(),
                                           Constants.OUTPUT_FILE: output_file})
            return True
    except Exception as e:
        log.error(e)
        update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.FAILED, Constants.EXTRACT_END: datetime.now()})
        return False


@celery.task(name="tasks.extract.remote_copy",
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def archive(zip_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''
    prepare_path(zip_file_name)
    archive_files(zip_file_name, directory)


@celery.task(name="tasks.extract.remote_copys",
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def remote_copy(src_file_name, hostname, tenant, gatekeeper, sftp_user, private_key_path):
    #TODO check return code
    copy(src_file_name, hostname, tenant, gatekeeper, sftp_user, private_key_path)
