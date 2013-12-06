'''
Celery Tasks for data extraction

Created on Nov 5, 2013

@author: ejen
'''
import logging
from smarter.reports.helpers.constants import Constants
from smarter.extract.constants import Constants as Extract, ExtractType
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.extract.student_assessment import get_extract_assessment_query, compile_query_to_sql_text
from pyramid.security import authenticated_userid
from uuid import uuid4
from edextract.status.status import create_new_entry
from edextract.tasks.extract import start_extract, archive, route_tasks
from pyramid.threadlocal import get_current_request, get_current_registry
from datetime import datetime
import os
import tempfile
from edapi.exceptions import NotFoundException
import copy
from smarter.security.context import select_with_context
from sqlalchemy.sql.expression import and_
from smarter.extract.metadata import get_metadata_file_name, get_asmt_metadata


log = logging.getLogger('smarter')


def process_sync_extract_request(params):
    tasks = []
    request_id, user, tenant = __get_extract_request_user_info()
    extract_params = copy.deepcopy(params)
    for subject in params[Constants.ASMTSUBJECT]:
        extract_params[Constants.ASMTSUBJECT] = subject
        subject_tasks, task_responses = __create_tasks_with_responses(request_id, user, tenant, extract_params)
        tasks += subject_tasks

    if len(tasks) > 0:
        directory_to_archive = get_extract_work_zone_path(tenant, request_id)
        celery_timeout = int(get_current_registry().settings.get('extract.celery_timeout', '30'))
        # Synchronous calls to generate json and csv and then to archive
        route_tasks(tenant, request_id, tasks, 'extract-sync')().get(timeout=celery_timeout)
        result = archive.apply_async(args=[request_id, directory_to_archive], queue='extract_sync')
        return result.get(timeout=celery_timeout)
    else:
        raise NotFoundException("There are no results")


def process_async_extraction_request(params):
    '''
    :param dict params: contains query parameter.  Value for each pair is expected to be a list
    '''
    tasks = []
    response = {}
    task_responses = []
    request_id, user, tenant = __get_extract_request_user_info()

    for s in params[Constants.ASMTSUBJECT]:
        for t in params[Constants.ASMTTYPE]:
            # TODO: handle year and stateCode/tenant
            param = ({Constants.ASMTSUBJECT: s,
                     Constants.ASMTTYPE: t,
                     Constants.ASMTYEAR: params[Constants.ASMTYEAR][0],
                     Constants.STATECODE: params[Constants.STATECODE][0],
                     Extract.EXTRACT_LEVEL: params.get(Extract.EXTRACT_LEVEL, '')})

            task_response = {Constants.STATECODE: param[Constants.STATECODE],
                             Extract.EXTRACTTYPE: ExtractType.studentAssessment,
                             Constants.ASMTSUBJECT: param[Constants.ASMTSUBJECT],
                             Constants.ASMTTYPE: param[Constants.ASMTTYPE],
                             # Constants.ASMTYEAR: task[Constants.ASMTYEAR],
                             Extract.REQUESTID: request_id}

            # separate by grades if no grade is specified
            __tasks, __task_responses = __create_tasks_with_responses(request_id, user, tenant, param, task_response)
            tasks += __tasks
            task_responses += __task_responses

    response['tasks'] = task_responses
    if len(tasks) > 0:
        # TODO: handle empty public key
        public_key_id = get_encryption_public_key_identifier(tenant)
        archive_file_name = get_archive_file_path(user.get_uid(), tenant, request_id)
        response['fileName'] = os.path.basename(archive_file_name)
        directory_to_archive = get_extract_work_zone_path(tenant, request_id)
        gatekeeper_id = get_gatekeeper(tenant)
        pickup_zone_info = get_pickup_zone_info(tenant)
        start_extract.apply_async(args=[tenant, request_id, public_key_id, archive_file_name, directory_to_archive, gatekeeper_id, pickup_zone_info, tasks], queue='extract')  # @UndefinedVariable
    return response


def __parepare_data(param):
    asmt_guids = []
    available_grades = []
    with EdCoreDBConnection() as connector:
        asmt_type = param.get(Constants.ASMTTYPE)
        asmt_subject = param.get(Constants.ASMTSUBJECT)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select_with_context([dim_asmt.c.asmt_guid.label(Constants.ASMTGUID)], from_obj=[dim_asmt])
        query = query.where(and_(dim_asmt.c.asmt_type == asmt_type)).where(and_(dim_asmt.c.asmt_subject == asmt_subject))
        results = connector.get_result(query)
        for result in results:
            asmt_guids.append(result[Constants.ASMTGUID])
    asmt_grade = param.get(Constants.ASMTGRADE)
    if asmt_grade is None:
        available_grades = get_current_registry().settings.get('extract.available_grades', '').split(',')
    else:
        available_grades = [asmt_grade]
    return asmt_guids, available_grades, dim_asmt, fact_asmt_outcome


def __create_tasks_with_responses(request_id, user, tenant, param, task_response={}):
    tasks = []
    task_responses = []
    copied_task_response = copy.deepcopy(task_response)
    asmt_guids, available_grades, dim_asmt, fact_asmt_outcome = __parepare_data(param)

    # 1. check record availability
    # if asmt_grade is already set value, then set to None.
    param[Constants.ASMTGRADE] = None
    query = get_extract_assessment_query(param)
    if has_data(query.limit(1), request_id):
        # 2. check data by asmt_guids
        for asmt_guid in asmt_guids:
            copied_params = copy.deepcopy(param)
            copied_params[Constants.ASMTGUID] = asmt_guid
            query_with_asmt_guid = query.where(and_(dim_asmt.c.asmt_guid == asmt_guid))
            if has_data(query_with_asmt_guid.limit(1), request_id):
                # 3. check asmt_grade
                for asmt_grade in available_grades:
                    copied_params[Constants.ASMTGRADE] = asmt_grade
                    query_with_asmt_guid_and_asmt_grade = query_with_asmt_guid.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
                    if has_data(query_with_asmt_guid_and_asmt_grade.limit(1), request_id):
                        tasks += (__create_tasks(request_id, user, tenant, copied_params, query_with_asmt_guid_and_asmt_grade))
        copied_task_response[Extract.STATUS] = Extract.OK
        task_responses.append(copied_task_response)
    else:
        copied_task_response[Extract.STATUS] = Extract.FAIL
        copied_task_response[Extract.MESSAGE] = "Data is not available"
        task_responses.append(copied_task_response)
    return tasks, task_responses


def has_data(query, request_id):
    log.info('Extract: data availability check for request ' + request_id)
    with EdCoreDBConnection() as connection:
        result = connection.get_result(query)
    if result is None or len(result) < 1:
        return False
    else:
        return True


def __create_tasks(request_id, user, tenant, params, query):
    tasks = []
    tasks.append(__create_new_task(request_id, user, tenant, params, query))
    tasks.append(__create_asmt_metadata_task(request_id, user, tenant, params))
    return tasks


def __create_asmt_metadata_task(request_id, user, tenant, params):
    query = get_asmt_metadata(params.get(Constants.ASMTGUID))
    return __create_new_task(request_id, user, tenant, params, query, asmt_metadata=True)


def __create_new_task(request_id, user, tenant, params, query, asmt_metadata=False):
    task = {}
    task['task_id'] = create_new_entry(user, request_id, params)
    if asmt_metadata:
        task['file_name'] = get_asmt_metadata_file_path(params, tenant, request_id)
        task['is_json_request'] = False
    else:
        task['file_name'] = get_extract_file_path(params, tenant, request_id)
        task['is_json_request'] = True
    task['query'] = compile_query_to_sql_text(query)
    return task


def __get_extract_request_user_info():
    # Generate an uuid for this extract request
    request_id = str(uuid4())
    user = authenticated_userid(get_current_request())
    tenant = user.get_tenant()
    return request_id, user, tenant


def __get_extract_work_zone_base_dir():
    return get_current_registry().settings.get('extract.work_zone_base_dir', tempfile.gettempdir())


def get_extract_work_zone_path(tenant, request_id):
    base = __get_extract_work_zone_base_dir()
    return os.path.join(base, tenant, request_id, 'csv')


def get_extract_file_path(param, tenant, request_id):
    asmtGrade = param.get(Constants.ASMTGRADE)
    if asmtGrade is not None:
        identifier = '_GRADE_' + str(asmtGrade)
    elif param.get(Constants.SCHOOLGUID) is not None:
        identifier = ''
    else:
        identifier = '_' + param.get(Constants.STATECODE)

    tenant_level = param.get(Extract.EXTRACT_LEVEL, '')
    if tenant_level == Extract.TENANT:
        tenant_name = '_' + tenant
    else:
        tenant_name = ''
    file_name = 'ASMT{tenant_name}{identifier}_{asmtSubject}_{asmtType}_{currentTime}_{asmtGuid}.csv'.format(tenant_name=tenant_name,
                                                                                                             identifier=identifier.upper(),
                                                                                                             asmtSubject=param[Constants.ASMTSUBJECT].upper(),
                                                                                                             asmtType=param[Constants.ASMTTYPE].upper(),
                                                                                                             currentTime=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")),
                                                                                                             asmtGuid=param[Constants.ASMTGUID])
    return os.path.join(get_extract_work_zone_path(tenant, request_id), file_name)


def get_asmt_metadata_file_path(params, tenant, request_id):
    return os.path.join(get_extract_work_zone_path(tenant, request_id), get_metadata_file_name(params))


def get_encryption_public_key_identifier(tenant):
    return get_current_registry().settings.get('extract.gpg.public_key.' + tenant)


def get_archive_file_path(user_name, tenant, request_id):
    base = __get_extract_work_zone_base_dir()
    file_name = '{user_name}_{current_time}.zip.gpg'.format(user_name=user_name, current_time=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")))
    return os.path.join(base, tenant, request_id, 'zip', file_name)


def get_gatekeeper(tenant):
    '''
    Give a tenant name, return the path of gatekeeper's jail acct path

    :params string tenant:  name of tenant
    '''
    return get_current_registry().settings.get('pickup.gatekeeper.' + tenant)


def get_pickup_zone_info(tenant):
    '''
    Returns a tuple containing of sftp hostname, user, private key path
    '''
    reg = get_current_registry().settings
    server = reg.get('pickup.sftp.hostname', 'localhost')
    user = reg.get('pickup.sftp.user')
    private_key_path = reg.get('pickup.sftp.private_key_file')
    return (server, user, private_key_path)
