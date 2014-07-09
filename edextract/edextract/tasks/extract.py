'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''

import io
import os.path
import logging

from celery.canvas import chain, group

from edextract.celery import celery
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.settings.config import Config, get_setting
from edextract.utils import file_utils
from edextract.exceptions import ExtractionError
from edcore.exceptions import RemoteCopyError
from edcore.utils.utils import archive_files
from edextract.data_extract_generation.query_extract_generator import generate_csv, generate_json
from edextract.data_extract_generation.item_level_generator import generate_items_csv
from edextract.data_extract_generation.raw_data_generator import generate_raw_data_xml
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report
from edextract.tasks.constants import ExtractionDataType
from hpz_client.frs.http_file_upload import http_file_upload


log = logging.getLogger('edextract')
MAX_RETRY = get_setting(Config.MAX_RETRIES, 1)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY, 60)


@celery.task(name='task.extract.start_extract')
def start_extract(tenant, request_id, archive_file_names, directories_to_archive, registration_ids, tasks, queue=TaskConstants.DEFAULT_QUEUE_NAME):
    '''
    entry point to start an extract request for one or more extract tasks
    it groups the generation of csv into a celery task group and then chains it to the next task to archive the files into one zip
    '''
    workflow = chain(generate_prepare_path_task(request_id, archive_file_names, directories_to_archive, queue_name=queue),
                     generate_extract_file_tasks(tenant, request_id, tasks, queue_name=queue),
                     extract_group_separator.subtask(immutable=True),  # @UndefinedVariable
                     generate_archive_file_tasks(request_id, archive_file_names, directories_to_archive, queue_name=queue),
                     extract_group_separator.subtask(immutable=True),  # @UndefinedVariable
                     generate_remote_copy_tasks(request_id, archive_file_names, registration_ids, queue_name=queue))
    workflow.apply_async()

@celery.task(name="tasks.extract.separator")
def extract_group_separator():
    '''
    A dummy task to separate out a chain of two consecutive groups
    '''
    pass


def generate_prepare_path_task(request_id, archive_file_names, directories_to_archive, queue_name=TaskConstants.DEFAULT_QUEUE_NAME):
    """
    Given a list of paths, create a single celery task to prepare the paths

    @param request_id: Report request ID
    @param archive_file_names: list of the archive file names
    @param directories_to_archive: list of directories to be archived using the names in archive_file_names
    @param queue_name(optional): Queue to which to send celery task requests

    @return: Celery task to execute
    """
    paths_to_prepare = [directory for directory in directories_to_archive] + [os.path.dirname(file) for file in archive_file_names]
    return prepare_path.subtask(args=[request_id, paths_to_prepare], queue=queue_name, immutable=True)


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


def generate_extract_file_tasks(tenant, request_id, tasks, queue_name=TaskConstants.DEFAULT_QUEUE_NAME):
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
        extract_type = task.get(TaskConstants.EXTRACTION_DATA_TYPE)
        if extract_type in [ExtractionDataType.QUERY_ITEMS_CSV, ExtractionDataType.QUERY_RAW_XML]:
            generate_tasks.append(generate_item_or_raw_extract_file.subtask(args=[tenant, request_id, task], queue=queue_name, immutable=True))
        else:
            generate_tasks.append(generate_extract_file.subtask(args=[tenant, request_id, task], queue=queue_name, immutable=True))
    return group(generate_tasks)


@celery.task(name="tasks.extract.archive_with_stream")
def archive_with_stream(request_id, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    @return: Streamed contents of archive file.
    '''

    task_info = {Constants.TASK_ID: archive_with_stream.request.id,
                 Constants.CELERY_TASK_ID: archive_with_stream.request.id,
                 Constants.REQUEST_GUID: request_id}
    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVING})

    archive_memory_file = io.BytesIO()
    archive_files(directory, archive_memory_file)
    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVED})
    return archive_memory_file.getvalue()


def generate_archive_file_tasks(request_id, archive_file_names, directories_to_archive, queue_name=TaskConstants.DEFAULT_QUEUE_NAME):
    """
    Given a list of directories to archive and a corresponding list of archive file names, create a celery task for each
    one of the archiving to be done

    @param request_id: Report request ID
    @param archive_file_names: list of the archive file names
    @param directories_to_archive: list of directories to be archived using the names in archive_file_names
    @param queue_name(optional): Queue to which to send celery task requests

    @return: Group of celery tasks to execute
    """
    archive_tasks = []

    for i in range(0, len(directories_to_archive)):
        archive_tasks.append(archive.subtask(args=[request_id, archive_file_names[i], directories_to_archive[i]], queue=queue_name, immutable=True))
    return group(archive_tasks)


@celery.task(name="tasks.extract.archive", max_retries=MAX_RETRY, default_retry_delay=DEFAULT_RETRY_DELAY)
def archive(request_id, archive_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''
    try:
        task_info = {Constants.TASK_ID: archive.request.id,
                     Constants.CELERY_TASK_ID: archive.request.id,
                     Constants.REQUEST_GUID: request_id}

        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVING})
        archive_files(directory, archive_file_name)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.ARCHIVED})

    except Exception as e:
        # unrecoverable exception
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        raise ExtractionError()


def generate_remote_copy_tasks(request_id, archive_file_names, registration_ids, queue_name=TaskConstants.DEFAULT_QUEUE_NAME):
    """
    Given a list of archive files and a corresponding list of registration ids, create a celery task for each
    one of the remote copy to be done

    @param request_id: Report request ID
    @param archive_file_names: list of the archive file names
    @param registration_ids: list of registration ids obtained from HPZ corresponding to each file in the archive_file_names list
    @param queue_name(optional): Queue to which to send celery task requests

    @return: Group of celery tasks to execute
    """
    remote_copy_tasks = []

    for i in range(0, len(archive_file_names)):
        remote_copy_tasks.append(remote_copy.subtask(args=[request_id, archive_file_names[i], registration_ids[i]], queue=queue_name, immutable=True))
    return group(remote_copy_tasks)


@celery.task(name="tasks.extract.remote_copy", max_retries=MAX_RETRY, default_retry_delay=DEFAULT_RETRY_DELAY)
def remote_copy(request_id, src_file_name, registration_id):
    '''
    Remotely copies a source file to a remote machine
    '''
    task_info = {Constants.TASK_ID: remote_copy.request.id,
                 Constants.CELERY_TASK_ID: remote_copy.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPYING})
        http_file_upload(src_file_name, registration_id)
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
            raise remote_copy.retry(args=[request_id, src_file_name, registration_id], exc=exc)

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


@celery.task(name="tasks.extract.generate_item_or_raw_extract_file", max_retries=MAX_RETRY, default_retry_delay=DEFAULT_RETRY_DELAY)
def generate_item_or_raw_extract_file(tenant, request_id, task):
    """
    Generates an item level/raw extract file given task arguments.

    @param tenant: Tenant name
    @param request_id: Extract request ID
    @param task: Calling task
    """
    task_id = task[TaskConstants.TASK_TASK_ID]
    extract_type = task[TaskConstants.EXTRACTION_DATA_TYPE]
    log.info('execute {task_name} for task {task_id}, extract type {extract_type}'.format(task_name=generate_item_or_raw_extract_file.name,
                                                                                          task_id=task_id, extract_type=extract_type))
    output_dirs = task[TaskConstants.DIRECTORY_TO_ARCHIVE]
    output_files = task[TaskConstants.TASK_FILE_NAME]

    task_info = {Constants.TASK_ID: task_id,
                 Constants.CELERY_TASK_ID: generate_item_or_raw_extract_file.request.id,
                 Constants.REQUEST_GUID: request_id}
    retryable = False
    exception_thrown = False
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTING})
        if tenant is None:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED_NO_TENANT})
        else:
            if extract_type is ExtractionDataType.QUERY_ITEMS_CSV:
                for output_file in output_files:
                    if not os.path.isdir(os.path.dirname(output_file)):
                        raise FileNotFoundError(os.path.dirname(output_file) + " doesn't exist")
            if extract_type is ExtractionDataType.QUERY_RAW_XML:
                for output_dir in output_dirs:
                    if not os.path.isdir(output_dir):
                        raise FileNotFoundError(output_dir + " doesn't exist")

            # for item level the output path is a list of one or more files
            # and for raw extract the output path is a list of one or more directory
            # to place all the matching xml files
            if extract_type == ExtractionDataType.QUERY_ITEMS_CSV:
                output_paths = output_files
            else:
                output_paths = output_dirs
            # Extract data to file
            extract_func = get_extract_func(extract_type)
            extract_func(tenant, output_paths, task_info, task)

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
        ExtractionDataType.QUERY_RAW_XML: generate_raw_data_xml,
        ExtractionDataType.SR_STATISTICS: generate_statistics_report,
        ExtractionDataType.SR_COMPLETION: generate_completion_report
    }

    return extract_funcs[extract_type]
