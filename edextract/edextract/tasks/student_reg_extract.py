__author__ = 'tshewchuk'

"""
This module contains the tasks specific to student registration report extraction.
"""

import os.path
import logging

from celery.canvas import chain
from edextract.tasks.student_reg_constants import Constants as TaskConstants, ReportType
from edextract.tasks.extract import prepare_path, archive_with_encryption, remote_copy
from edextract.celery import celery
from edextract.tasks.extract import generate_extract_file
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report


log = logging.getLogger('edstudentregextract')


@celery.task(name='task.extract.start_sr_extract')
def start_extract(tenant, request_id, public_key_id, encrypted_archive_file_name, directory_to_archive, gatekeeper_id, pickup_zone_info, report_task, queue=TaskConstants.DEFAULT_QUEUE_NAME):
    """
    This is the entry point to start an extract request.
    It creates the chain to extract, zip, encrypt and copy the report extract file.

    @param tenant: tenant of the user
    @param request_id: Report request ID
    @param public_key_id: Encryption public key
    @param encrypted_archive_file_name: Encrypted archive file name
    @param directory_to_archive: Directory into ehich teh encrypted archive file is placed
    """

    task_id = report_task[TaskConstants.TASK_TASK_ID]
    output_file = report_task[TaskConstants.TASK_FILE_NAME]
    extract_args = {TaskConstants.STATE_CODE: report_task[TaskConstants.STATE_CODE], TaskConstants.ACADEMIC_YEAR: report_task[TaskConstants.ACADEMIC_YEAR]}
    report_type = report_task[TaskConstants.REPORT_TYPE]
    if report_type == ReportType.STATISTICS:
        extract_func = generate_statistics_report
    elif report_type == ReportType.COMPLETION:
        extract_func = generate_completion_report
    else:
        raise ValueError('Invalid report type')

    workflow = chain(prepare_path.subtask(args=[tenant, request_id, [directory_to_archive, os.path.dirname(encrypted_archive_file_name)]], queues=queue, immutable=True),
                     generate_extract_file.subtask(args=[tenant, request_id, task_id, output_file, extract_func, extract_args], queues=queue, immutable=True),
                     archive_with_encryption.subtask(args=[request_id, public_key_id, encrypted_archive_file_name, directory_to_archive], queues=queue, immutable=True),
                     remote_copy.subtask(args=[request_id, encrypted_archive_file_name, tenant, gatekeeper_id, pickup_zone_info], queues=queue, immutable=True))
    workflow.apply_async()
