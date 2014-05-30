'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''

import os.path
import logging
from edextract.celery import celery
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.settings.config import Config, get_setting
from edextract.utils import file_utils
from celery.canvas import chain, group
from edextract.utils.file_remote_copy import copy
from edextract.exceptions import ExtractionError
from edcore.exceptions import RemoteCopyError
from edextract.utils.data_archiver import encrypted_archive_files, archive_files, GPGPublicKeyException
from edextract.data_extract_generation.query_extract_generator import generate_csv, generate_json
from edextract.data_extract_generation.item_level_generator import generate_items_csv
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report
from edextract.tasks.constants import ExtractionDataType


log = logging.getLogger('edextract')
MAX_RETRY = get_setting(Config.MAX_RETRIES, 1)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY, 60)


@celery.task(name='task.extract.start_extract')
def start_extract(tenant, request_id, public_key_id, archive_file_name, directory_to_archive, gatekeeper_id, pickup_zone_info, tasks, queue=TaskConstants.DEFAULT_QUEUE_NAME):
    '''
    entry point to start an extract request for one or more extract tasks
    it groups the generation of csv into a celery task group and then chains it to the next task to archive the files into one zip
    '''
    ##### TODO: Remove this section once extraction is fully integrated with HPZ.
    # This is a temporary hack to gradually replace encryption and remote copying to SFTP zone with HTTP transfer via HPZ.
    hpz_extract_types = [ExtractionDataType.SR_STATISTICS, ExtractionDataType.SR_COMPLETION]
    extract_type = tasks[0][TaskConstants.EXTRACTION_DATA_TYPE]
    if True:  # Just until FTs are updated.
    #if extract_type not in hpz_extract_types:
        workflow = chain(prepare_path.subtask(args=[request_id, [directory_to_archive, os.path.dirname(archive_file_name)]], queues=queue, immutable=True),
                         generate_extract_file_tasks(tenant, request_id, tasks, queue_name=queue),
                         archive_with_encryption.subtask(args=[request_id, public_key_id, archive_file_name, directory_to_archive], queues=queue, immutable=True),
                         remote_copy.subtask(args=[request_id, archive_file_name, tenant, gatekeeper_id, pickup_zone_info], queues=queue, immutable=True))
    else:
    #####
    ##### TODO: Retain this section once extraction is fully integrated with HPZ.
        workflow = chain(prepare_path.subtask(args=[request_id, [directory_to_archive, os.path.dirname(archive_file_name)]], queues=queue, immutable=True),
                         generate_extract_file_tasks(tenant, request_id, tasks, queue_name=queue),
                         archive.subtask(args=[request_id, public_key_id, archive_file_name, directory_to_archive], queues=queue, immutable=True))
    #####

    workflow.apply_async()


@celery.task(name='task.extract.prepare_path')
def prepare_path(request_id, paths):
    '''
    Given a list of paths of directories, creates it if it doesn't exist
    '''
    task_info = {Constants.TASK_ID: prepare_path.request.id,
                 Constants.CELERY_TASK_ID: prepare_path.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        for path in paths:
            file_utils.prepare_path(path)
    except FileNotFoundError as e:
        # which thrown from prepare_path
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        raise ExtractionError()


def generate_extract_file_tasks(tenant, request_id, tasks, queue_name=TaskConstants.DEFAULT_QUEUE_NAME,
                                item_level=False):
    """
    Given a list of tasks, create a celery task for each one to generate the task-specific extract file.

    @param tenant: tenant of the user
    @param request_id: Report request ID
    @param tasks: List of extract tasks to execute
    @param queue_name(optional): Queue to which to send celery task requests

    @return: Group of celery tasks to execute
    """

    generate_tasks = []

    for task in tasks:
        if item_level:
            generate_tasks.append(generate_item_level_extract_file.subtask(args=[tenant, request_id, task], queue=queue_name, immutable=True))
        else:
            generate_tasks.append(generate_extract_file.subtask(args=[tenant, request_id, task], queue=queue_name, immutable=True))

    return group(generate_tasks)


@celery.task(name="tasks.extract.archive")
def archive(request_id, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''
    task_info = {Constants.TASK_ID: archive.request.id,
                 Constants.CELERY_TASK_ID: archive.request.id,
                 Constants.REQUEST_GUID: request_id}
    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVING})
    content = archive_files(directory)
    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVED})
    return content.getvalue()


# TODO: Remove this task once all extract types are downloaded by HPZ.
@celery.task(name="tasks.extract.archive_with_encryption",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def archive_with_encryption(request_id, recipients, encrypted_archive_file_name, directory):
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
        encrypted_archive_files(directory, recipients, encrypted_archive_file_name, homedir=homedir, keyserver=keyserver, gpgbinary=gpg_binary_file)
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
                raise archive_with_encryption.retry(args=[request_id, recipients, encrypted_archive_file_name, directory], exc=exc)
        else:
            raise ExtractionError()


# TODO: Remove this task once all extract types are downloaded by HPZ.
@celery.task(name="tasks.extract.remote_copy",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def remote_copy(request_id, src_file_name, tenant, gatekeeper, sftp_info, timeout=1800):
    '''
    Remotely copies a source file to a remote machine
    '''
    task_info = {Constants.TASK_ID: remote_copy.request.id,
                 Constants.CELERY_TASK_ID: remote_copy.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPYING})
        copy(src_file_name, sftp_info[0], tenant, gatekeeper, sftp_info[1], sftp_info[2], timeout=timeout)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPIED})
    except RemoteCopyError as e:
        log.error("Exception happened in remote copy. " + str(e))
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: 'remote copy has failed: ' + str(e)})
        try:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            raise ExtractionError(str(e))
        except ExtractionError as exc:
            # this could be caused by network hiccup
            raise remote_copy.retry(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info], kwargs={'timeout': timeout}, exc=exc)
    except Exception as e:
        raise ExtractionError(str(e))


@celery.task(name="tasks.extract.generate_extract_file", max_retries=MAX_RETRY, default_retry_delay=DEFAULT_RETRY_DELAY)
def generate_extract_file(tenant, request_id, task):
    """
    Generates an extract file given task arguments.

    @param tenant: Tenant name
    @param request_id: Extract request ID
    @param task: Calling task
    @param extract_type: Specific type of data extract for calling task
    """

    task_id = task[TaskConstants.TASK_TASK_ID]
    extract_type = task[TaskConstants.EXTRACTION_DATA_TYPE]
    log.info('execute {task_name} for task {task_id}, extract type {extract_type}'.format(task_name=generate_extract_file.name,
                                                                                          task_id=task_id, extract_type=extract_type))
    output_file = task[TaskConstants.TASK_FILE_NAME]
    task_info = {Constants.TASK_ID: task_id,
                 Constants.CELERY_TASK_ID: generate_extract_file.request.id,
                 Constants.REQUEST_GUID: request_id}
    retryable = False
    exception_thrown = False

    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTING})
        if tenant is None:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED_NO_TENANT})
        else:
            if not os.path.isdir(os.path.dirname(output_file)):
                raise FileNotFoundError(os.path.dirname(output_file) + " doesn't exist")

            # Extract data to file.
            extract_func = get_extract_func(extract_type)
            extract_func(tenant, output_file, task_info, task)

    except FileNotFoundError as e:
        # which thrown from prepare_path
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
        retryable = False

    except Exception as e:
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
        retryable = True

    if exception_thrown:
        if retryable:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            try:
                raise ExtractionError()
            except ExtractionError as exc:
                raise generate_extract_file.retry(args=[tenant, request_id, task], exc=exc)
        else:
            raise ExtractionError()


@celery.task(name="tasks.extract.generate_item_level_extract_file", max_retries=MAX_RETRY, default_retry_delay=DEFAULT_RETRY_DELAY)
def generate_item_level_extract_file(tenant, request_id, task):
    """
    Generates an extract file given task arguments.

    @param tenant: Tenant name
    @param request_id: Extract request ID
    @param task: Calling task
    @param extract_type: Specific type of data extract for calling task
    """

    task_id = task[TaskConstants.TASK_TASK_ID]
    extract_type = task[TaskConstants.EXTRACTION_DATA_TYPE]
    log.info('execute {task_name} for task {task_id}, extract type {extract_type}'.format(task_name=generate_item_level_extract_file.name,
                                                                                          task_id=task_id, extract_type=extract_type))
    output_file = task[TaskConstants.TASK_FILE_NAME]
    task_info = {Constants.TASK_ID: task_id,
                 Constants.CELERY_TASK_ID: generate_item_level_extract_file.request.id,
                 Constants.REQUEST_GUID: request_id}
    retryable = False
    exception_thrown = False

    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTING})
        if tenant is None:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED_NO_TENANT})
        else:
            if not os.path.isdir(os.path.dirname(output_file)):
                raise FileNotFoundError(os.path.dirname(output_file) + " doesn't exist")

            # Extract data to file.
            extract_func = get_extract_func(extract_type)
            extract_func(tenant, output_file, task_info, task)

    except FileNotFoundError as e:
        # which thrown from prepare_path
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
        retryable = False

    except Exception as e:
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
        retryable = True

    if exception_thrown:
        if retryable:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            try:
                raise ExtractionError()
            except ExtractionError as exc:
                raise generate_extract_file.retry(args=[tenant, request_id, task], exc=exc)
        else:
            raise ExtractionError()


def get_extract_func(extract_type):
    extract_funcs = {
        ExtractionDataType.QUERY_CSV: generate_csv,
        ExtractionDataType.QUERY_JSON: generate_json,
        ExtractionDataType.QUERY_ITEMS_CSV: generate_items_csv,
        ExtractionDataType.SR_STATISTICS: generate_statistics_report,
        ExtractionDataType.SR_COMPLETION: generate_completion_report
    }

    return extract_funcs[extract_type]
