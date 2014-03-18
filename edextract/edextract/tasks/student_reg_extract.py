__author__ = 'tshewchuk'

"""
This module contains the tasks specific to student registration report extraction.
"""

import csv
import os.path
import logging
from celery.canvas import chain

from edextract.tasks.student_reg_constants import ReportType
from edextract.tasks.student_reg_constants import Constants as TaskConstants
from edextract.status.constants import Constants
from edextract.tasks.extract import MAX_RETRY, DEFAULT_RETRY_DELAY, prepare_path, archive_with_encryption, remote_copy
from edextract.celery import celery
from edextract.utils.student_reg_report_generator import generate_sr_statistics_report_data, generate_sr_completion_report_data
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.exceptions import ExtractionError


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

    workflow = chain(prepare_path.subtask(args=[tenant, request_id, [directory_to_archive, os.path.dirname(encrypted_archive_file_name)]], queues=queue, immutable=True),
                     generate_csv.subtask(args=[tenant, request_id, report_task[TaskConstants.TASK_TASK_ID], report_task[TaskConstants.REPORT_TYPE], report_task[TaskConstants.STATE_CODE],
                                          report_task[TaskConstants.ACADEMIC_YEAR], report_task[TaskConstants.TASK_FILE_NAME]], queues=queue, immutable=True),
                     archive_with_encryption.subtask(args=[request_id, public_key_id, encrypted_archive_file_name, directory_to_archive], queues=queue, immutable=True),
                     remote_copy.subtask(args=[request_id, encrypted_archive_file_name, tenant, gatekeeper_id, pickup_zone_info], queues=queue, immutable=True))
    workflow.apply_async()


@celery.task(name="tasks.extract.generate_sr_csv",
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def generate_csv(tenant, request_id, task_id, report_type, state_code, academic_year, output_file):
    """
    This is the celery entry point to execute data extraction query for student registration report.
    It writes the report data into the specified csv file.

    @param tenant: tenant of the user
    @param request_id: Report request ID
    @param task_id: Report data extract task ID
    @param output_file: CSV output file name
    """

    task_info = {Constants.TASK_ID: task_id,
                 Constants.CELERY_TASK_ID: generate_csv.request.id,
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

            with open(output_file, 'w') as csvfile:
                if report_type == ReportType.STATISTICS:
                    header, data = generate_sr_statistics_report_data(state_code, academic_year)
                elif report_type == ReportType.COMPLETION:
                    header, data = generate_sr_completion_report_data(state_code, academic_year)
                else:
                    raise ExtractionError('Invalid report type')

                csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
                csvwriter.writerow(header)
                for row in data:
                    csvwriter.writerow(row)
                insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})

    except FileNotFoundError as e:
        # which thrown from prepare_path
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True

    except ExtractionError as e:
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        exception_thrown = True

    except Exception as e:
        if os.path.isfile(output_file):
            # file should be deleted if there is an error
            os.unlink(output_file)
        log.error(e)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: str(e)})
        retryable = True
        exception_thrown = True

    if exception_thrown:
        if retryable:
            # this looks funny to you, but this is just a working around solution for celery bug
            # since exc option is not really working for retry.
            try:
                raise ExtractionError()
            except ExtractionError as exc:
                raise generate_csv.retry(args=[tenant, request_id, task_id, report_type, state_code, academic_year, output_file], exc=exc)
        else:
            raise ExtractionError()
