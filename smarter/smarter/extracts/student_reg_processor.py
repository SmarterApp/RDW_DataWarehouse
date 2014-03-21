from datetime import datetime
from edextract.status.status import create_new_entry
from smarter.extracts import processor

__author__ = 'tshewchuk'

"""
This module provides methods for extracting student registration report information into archive files for the user.
"""

import logging
import os
import pyramid.threadlocal

from smarter.extracts.constants import Constants as Extract, ExtractType
from edextract.tasks.constants import Constants as TaskConstants, ReportType
from smarter.reports.helpers.constants import Constants as EndpointConstants
from edextract.tasks.student_reg_extract import start_extract
from pyramid.threadlocal import get_current_registry


log = logging.getLogger('smarter')


def process_async_extraction_request(params):
    """
    @param params: Extract request parameters

    @return:  Extract response
    """

    queue = pyramid.threadlocal.get_current_registry().settings.get('extract.job.queue.async', TaskConstants.DEFAULT_QUEUE_NAME)
    response = {}
    request_id, user, tenant = processor.get_extract_request_user_info()

    extract_params = {TaskConstants.STATE_CODE: params[EndpointConstants.STATECODE][0],
                      TaskConstants.ACADEMIC_YEAR: params[EndpointConstants.ACADEMIC_YEAR][0],
                      TaskConstants.REPORT_TYPE: ReportType.STATISTICS}

    task_response = {TaskConstants.STATE_CODE: extract_params[TaskConstants.STATE_CODE],
                     TaskConstants.ACADEMIC_YEAR: extract_params[TaskConstants.ACADEMIC_YEAR],
                     Extract.EXTRACTTYPE: ExtractType.studentRegistrationStatistics,
                     Extract.REQUESTID: request_id,
                     Extract.STATUS: Extract.OK}

    task_info = _create_task_info(request_id, user, tenant, extract_params)

    response['tasks'] = [task_response]

    public_key_id = processor.get_encryption_public_key_identifier(tenant)
    archive_file_name = processor.get_archive_file_path(user.get_uid(), tenant, request_id)
    response['fileName'] = os.path.basename(archive_file_name)
    directory_to_archive = processor.get_extract_work_zone_path(tenant, request_id)
    gatekeeper_id = processor.get_gatekeeper(tenant)
    pickup_zone_info = processor.get_pickup_zone_info(tenant)

    start_extract.apply_async(args=[tenant, request_id, public_key_id, archive_file_name, directory_to_archive, gatekeeper_id, pickup_zone_info, task_info], queue=queue)
    return response


def _create_task_info(request_id, user, tenant, extract_params):
    task_info = {TaskConstants.TASK_TASK_ID: create_new_entry(user, request_id, extract_params),
                 TaskConstants.TASK_FILE_NAME: _get_extract_file_path(extract_params, tenant, request_id)}
    task_info.update(extract_params)

    return task_info


def _get_extract_file_path(params, tenant, request_id):
    file_name = '{stateCode}_{academicYear}_{currentTime}_STATS.csv'.format(stateCode=params.get(TaskConstants.STATE_CODE),
                                                                            academicYear=params.get(TaskConstants.ACADEMIC_YEAR),
                                                                            currentTime=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")))
    return os.path.join(processor.get_extract_work_zone_path(tenant, request_id), file_name)
