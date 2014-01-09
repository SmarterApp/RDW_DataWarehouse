'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''
import csv
import os.path
import logging
from edextract.celery import celery
from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.status.status import ExtractStatus, \
    insert_extract_stats
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.settings.config import Config, get_setting
from edextract.utils import file_utils
from celery.canvas import chain, group
from edextract.utils.file_remote_copy import copy
from edextract.exceptions import RemoteCopyError, ExtractionError
from edextract.utils.data_archiver import encrypted_archive_files, archive_files, \
    GPGPublicKeyException
import json
from edextract.utils.json_formatter import format_json


log = logging.getLogger('edextract')
MAX_RETRY = get_setting(Config.MAX_RETRIES)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY)


@celery.task(name='task.extract.start_extract')
def start_extract(tenant, request_id, public_key_id, encrypted_archive_file_name, directory_to_archive, gatekeeper_id, pickup_zone_info, tasks, queue=TaskConstants.DEFAULT_QUEUE_NAME):
    '''
    entry point to start an extract request for one or more extract tasks
    it groups the generation of csv into a celery task group and then chains it to the next task to archive the files into one zip
    '''
    workflow = chain(prepare_path.subtask(args=[tenant, request_id, [directory_to_archive, os.path.dirname(encrypted_archive_file_name)]], queues=queue, immutable=True),
                     route_tasks(tenant, request_id, tasks, queue_name=queue),
                     archive_with_encryption.subtask(args=[request_id, public_key_id, encrypted_archive_file_name, directory_to_archive], queues=queue, immutable=True),
                     remote_copy.subtask(args=[request_id, encrypted_archive_file_name, tenant, gatekeeper_id, pickup_zone_info], queues=queue, immutable=True))
    workflow.apply_async()


@celery.task(name='task.extract.prepare_path')
def prepare_path(tenant, request_id, paths):
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


def route_tasks(tenant, request_id, tasks, queue_name=TaskConstants.DEFAULT_QUEUE_NAME):
    '''
    Given a list of tasks, route them to either generate_csv or generate_json depending on the task type
    '''
    generate_tasks = []
    for task in tasks:
        celery_task = generate_json if task.get(TaskConstants.TASK_IS_JSON_REQUEST, False) else generate_csv
        generate_tasks.append(celery_task.subtask(args=[tenant, request_id, task[TaskConstants.TASK_TASK_ID], task[TaskConstants.TASK_QUERY], task[TaskConstants.TASK_FILE_NAME]], queue=queue_name, immutable=True))  # @UndefinedVariable
    return group(generate_tasks)


@celery.task(name="tasks.extract.generate_csv",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def generate_csv(tenant, request_id, task_id, query, output_file):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param tenant: tenant of the user
    :param query: extraction query to dump data
    :param params: request extraction input parameters
    :param output_uri: output file uri
    :param batch_id: batch_id for tracking
    '''
    log.info('execute tasks.extract.generate_csv for task ' + task_id)
    task_info = {Constants.TASK_ID: task_id,
                 Constants.CELERY_TASK_ID: generate_csv.request.id,
                 Constants.REQUEST_GUID: request_id}
    retriable = False
    exception_thrown = False
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTING})
        if tenant is None:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED_NO_TENANT})
        else:
            if not os.path.isdir(os.path.dirname(output_file)):
                raise FileNotFoundError(os.path.dirname(output_file) + " doesn't exist")
            with EdCoreDBConnection(tenant) as connection, open(output_file, 'w') as csvfile:
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
    except FileNotFoundError as e:
        # which thrown from prepare_path
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
    except Exception as e:
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        retriable = True
        exception_thrown = True

    if exception_thrown:
        if retriable:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            try:
                raise ExtractionError()
            except ExtractionError as exc:
                raise generate_csv.retry(args=[tenant, request_id, task_id, query, output_file], exc=exc)
        else:
            raise ExtractionError()


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


@celery.task(name="tasks.extract.archive_with_encryption",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def archive_with_encryption(request_id, recipients, encrypted_archive_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''
    retriable = False
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
        retriable = True
        exception_thrown = True
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
    except Exception as e:
        # unrecoverable exception
        exception_thrown = True
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})

    if exception_thrown:
        if retriable:
            try:
                # this looks funny to you, but this is just a working around solution for celery bug
                # since exc option is not really working for retry.
                raise ExtractionError()
            except ExtractionError as exc:
                raise archive_with_encryption.retry(args=[request_id, recipients, encrypted_archive_file_name, directory], exc=exc)
        else:
            raise ExtractionError()


@celery.task(name="tasks.extract.remote_copy",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def remote_copy(request_id, src_file_name, tenant, gatekeeper, sftp_info):
    '''
    Remotely copies a source file to a remote machine
    '''
    task_info = {Constants.TASK_ID: remote_copy.request.id,
                 Constants.CELERY_TASK_ID: remote_copy.request.id,
                 Constants.REQUEST_GUID: request_id}
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.COPYING})
        copy(src_file_name, sftp_info[0], tenant, gatekeeper, sftp_info[1], sftp_info[2])
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
            raise remote_copy.retry(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info], exc=exc)
    except Exception as e:
        raise ExtractionError(str(e))


@celery.task(name="tasks.extract.generate_json",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def generate_json(tenant, request_id, task_id, query, output_file):
    '''
    Generates a json file given a result from the first element of a query
    '''
    task_info = {Constants.TASK_ID: task_id,
                 Constants.CELERY_TASK_ID: generate_json.request.id,
                 Constants.REQUEST_GUID: request_id}
    retriable = False
    exception_thrown = False
    try:
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.GENERATING_JSON})
        if tenant is None:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED_NO_TENANT})
        else:
            if not os.path.isdir(os.path.dirname(output_file)):
                raise FileNotFoundError(os.path.dirname(output_file) + " doesn't exist")
            with EdCoreDBConnection(tenant) as connection, open(output_file, 'w') as outfile:
                results = connection.get_result(query)
                # There should only be one result in the list
                if len(results) is 1:
                    formatted = format_json(results[0])
                    json.dump(formatted, outfile, indent=4)
                    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.GENERATED_JSON})
                else:
                    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: "Results length is: " + str(len(results))})
    except FileNotFoundError as e:
        # which thrown from prepare_path
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
        retriable = False
    except Exception as e:
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True
        retriable = True

    if exception_thrown:
        if retriable:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            try:
                raise ExtractionError()
            except ExtractionError as exc:
                raise generate_json.retry(args=[tenant, request_id, task_id, query, output_file], exc=exc)
        else:
            raise ExtractionError()
