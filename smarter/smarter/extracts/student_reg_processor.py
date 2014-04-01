from edcore.utils.utils import compile_query_to_sql_text

__author__ = 'ablum'

"""
This module provides methods for extracting student registration report information into archive files for the user.
"""

import logging
import os
from datetime import datetime
from pyramid.threadlocal import get_current_registry

from smarter.extracts.constants import Constants as Extract, ExtractType, ReportType
from edextract.tasks.constants import Constants as TaskConstants, ExtractionDataType
from smarter.reports.helpers.constants import Constants as EndpointConstants
from edextract.tasks.extract import start_extract
from edextract.status.status import create_new_entry
from smarter.extracts import processor
from smarter.extracts.student_reg_statistics import get_headers, get_academic_year_query, get_match_id_query


log = logging.getLogger('smarter')


def process_async_extraction_request(params):
    """
    @param params: Extract request parameters

    @return:  Extract response
    """

    queue = get_current_registry().settings.get('extract.job.queue.async', TaskConstants.DEFAULT_QUEUE_NAME)
    response = {}
    state_code = params[EndpointConstants.STATECODE][0]
    request_id, user, tenant = processor.get_extract_request_user_info(state_code)

    extract_params = {TaskConstants.STATE_CODE: state_code,
                      TaskConstants.ACADEMIC_YEAR: params[EndpointConstants.ACADEMIC_YEAR][0],
                      Extract.REPORT_TYPE: ReportType.STATISTICS,
                      TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_STATISTICS}

    task_response = {TaskConstants.STATE_CODE: extract_params[TaskConstants.STATE_CODE],
                     TaskConstants.ACADEMIC_YEAR: extract_params[TaskConstants.ACADEMIC_YEAR],
                     Extract.EXTRACTTYPE: ExtractType.studentRegistrationStatistics,
                     Extract.REQUESTID: request_id,
                     Extract.STATUS: Extract.OK}

    task_info = _create_task_info(request_id, user, tenant, extract_params)

    response['tasks'] = [task_response]

    encrypted_file_path = processor.get_archive_file_path(user.get_uid(), tenant, request_id)
    response['fileName'] = os.path.basename(encrypted_file_path)

    data_directory_to_archive = processor.get_extract_work_zone_path(tenant, request_id)

    public_key_id = processor.get_encryption_public_key_identifier(tenant)
    gatekeeper_id = processor.get_gatekeeper(tenant)
    pickup_zone_info = processor.get_pickup_zone_info(tenant)

    start_extract.apply_async(args=[tenant, request_id, public_key_id, encrypted_file_path, data_directory_to_archive, gatekeeper_id, pickup_zone_info, [task_info]], queue=queue)

    return response


def _create_task_info(request_id, user, tenant, extract_params):
    academic_year_query = get_academic_year_query(extract_params[TaskConstants.ACADEMIC_YEAR], extract_params[TaskConstants.STATE_CODE])
    match_id_query = get_match_id_query(extract_params[TaskConstants.ACADEMIC_YEAR], extract_params[TaskConstants.STATE_CODE])

    task_info = {TaskConstants.TASK_TASK_ID: create_new_entry(user, request_id, extract_params),
                 TaskConstants.TASK_FILE_NAME: _get_extract_file_path(request_id, tenant, extract_params),
                 TaskConstants.CSV_HEADERS: get_headers(extract_params.get(TaskConstants.ACADEMIC_YEAR)),
                 TaskConstants.TASK_ACADEMIC_YEAR_QUERY: compile_query_to_sql_text(academic_year_query),
                 TaskConstants.TASK_MATCH_ID_QUERY: compile_query_to_sql_text(match_id_query)}
    task_info.update(extract_params)

    return task_info


def _get_extract_file_path(request_id, tenant, params):
    file_name = '{stateCode}_{academicYear}_{reportType}_{currentTime}.csv'.format(stateCode=params.get(TaskConstants.STATE_CODE),
                                                                                   academicYear=params.get(TaskConstants.ACADEMIC_YEAR),
                                                                                   reportType=params.get(Extract.REPORT_TYPE),
                                                                                   currentTime=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")))

    return os.path.join(processor.get_extract_work_zone_path(tenant, request_id), file_name)
