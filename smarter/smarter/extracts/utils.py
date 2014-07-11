'''
Created on Jul 9, 2014

@author: tosako
'''
from celery.canvas import chain, group
import os
from edextract.tasks.extract import prepare_path, archive, \
    generate_item_or_raw_extract_file, generate_extract_file, remote_copy, \
    extract_group_separator
from edextract.tasks.constants import Constants as TaskConstants, \
    ExtractionDataType


def start_extract(tenant, request_id, archive_file_names, directories_to_archive, registration_ids, tasks, queue=None):
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


def generate_prepare_path_task(request_id, archive_file_names, directories_to_archive, queue_name=None):
    """
    Given a list of paths, create a single celery task to prepare the paths

    @param request_id: Report request ID
    @param archive_file_names: list of the archive file names
    @param directories_to_archive: list of directories to be archived using the names in archive_file_names
    @param queue_name(optional): Queue to which to send celery task requests

    @return: Celery task to execute
    """
    paths_to_prepare = [directory for directory in directories_to_archive] + [os.path.dirname(file) for file in archive_file_names]
    return prepare_path.subtask(args=[request_id, paths_to_prepare], queue=queue_name, immutable=True)  # @UndefinedVariable


def generate_archive_file_tasks(request_id, archive_file_names, directories_to_archive, queue_name=None):
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
        archive_tasks.append(archive.subtask(args=[request_id, archive_file_names[i], directories_to_archive[i]], queue=queue_name, immutable=True))  # @UndefinedVariable
    return group(archive_tasks)


def generate_extract_file_tasks(tenant, request_id, tasks, queue_name=None):
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
            generate_tasks.append(generate_item_or_raw_extract_file.subtask(args=[tenant, request_id, task], queue=queue_name, immutable=True))  # @UndefinedVariable
        else:
            generate_tasks.append(generate_extract_file.subtask(args=[tenant, request_id, task], queue=queue_name, immutable=True))  # @UndefinedVariable
    return group(generate_tasks)


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
        remote_copy_tasks.append(remote_copy.subtask(args=[request_id, archive_file_names[i], registration_ids[i]], queue=queue_name, immutable=True))  # @UndefinedVariable
    return group(remote_copy_tasks)
