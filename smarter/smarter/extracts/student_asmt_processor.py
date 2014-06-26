from datetime import datetime
import os
import copy

from pyramid.threadlocal import get_current_registry
from sqlalchemy.sql.expression import and_

from smarter.extracts import processor
from smarter.reports.helpers.constants import Constants
from smarter.extracts.constants import Constants as Extract, ExtractType
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.extracts.student_assessment import get_extract_assessment_query, get_extract_assessment_item_and_raw_query
from edcore.utils.utils import compile_query_to_sql_text
from edcore.security.tenant import get_state_code_to_tenant_map
from edextract.status.status import create_new_entry
from edextract.tasks.extract import start_extract, archive_with_stream, generate_extract_file_tasks, prepare_path
from edapi.exceptions import NotFoundException
from smarter.security.context import select_with_context
from smarter.extracts.metadata import get_metadata_file_name, get_asmt_metadata
from edextract.tasks.constants import Constants as TaskConstants, ExtractionDataType, QueryType
from smarter_common.security.constants import RolesConstants
from hpz_client.frs.file_registration import register_file


__author__ = 'ablum'


def process_sync_extract_request(params):
    '''
    TODO add doc string
    '''
    settings = get_current_registry().settings
    queue = settings.get('extract.job.queue.sync', TaskConstants.SYNC_QUEUE_NAME)
    archive_queue = settings.get('extract.job.queue.archive', TaskConstants.ARCHIVE_QUEUE_NAME)
    tasks = []
    state_code = params[Constants.STATECODE]
    request_id, user, tenant = processor.get_extract_request_user_info(state_code)
    extract_params = copy.deepcopy(params)
    for subject in params[Constants.ASMTSUBJECT]:
        extract_params[Constants.ASMTSUBJECT] = subject
        subject_tasks, task_responses = _create_tasks_with_responses(request_id, user, tenant, extract_params)
        tasks += subject_tasks
    if tasks:
        directory_to_archive = processor.get_extract_work_zone_path(tenant, request_id)
        celery_timeout = int(get_current_registry().settings.get('extract.celery_timeout', '30'))
        # Synchronous calls to generate json and csv and then to archive
        # BUG, it still routes to 'extract' queue due to chain
#        result = chain(prepare_path.subtask(args=[tenant, request_id, [directory_to_archive]], queue=queue, immutable=True),      # @UndefinedVariable
#                       route_tasks(tenant, request_id, tasks, queue_name=queue),
#                       archive.subtask(args=[request_id, directory_to_archive], queue=archive_queue, immutable=True)).delay()
        prepare_path.apply_async(args=[request_id, [directory_to_archive]], queue=queue, immutable=True).get(timeout=celery_timeout)      # @UndefinedVariable
        generate_extract_file_tasks(tenant, request_id, tasks, queue_name=queue)().get(timeout=celery_timeout)
        result = archive_with_stream.apply_async(args=[request_id, directory_to_archive], queue=archive_queue, immutable=True)
        return result.get(timeout=celery_timeout)
    else:
        raise NotFoundException("There are no results")


def process_async_extraction_request(params, is_tenant_level=True):
    '''
    :param dict params: contains query parameter.  Value for each pair is expected to be a list
    :param bool is_tenant_level:  True if it is a tenant level request
    '''
    queue = get_current_registry().settings.get('extract.job.queue.async', TaskConstants.DEFAULT_QUEUE_NAME)
    tasks = []
    response = {}
    task_responses = []
    state_code = params[Constants.STATECODE][0]
    district_guid = params.get(Constants.DISTRICTGUID, [None])[0]
    request_id, user, tenant = processor.get_extract_request_user_info(state_code)

    for s in params[Constants.ASMTSUBJECT]:
        for t in params[Constants.ASMTTYPE]:
            param = ({Constants.ASMTSUBJECT: s,
                     Constants.ASMTTYPE: t,
                     Constants.ASMTYEAR: params[Constants.ASMTYEAR][0],
                     Constants.STATECODE: state_code,
                      Constants.DISTRICTGUID: district_guid})

            task_response = {Constants.STATECODE: param[Constants.STATECODE],
                             Constants.DISTRICTGUID: param[Constants.DISTRICTGUID],
                             Extract.EXTRACTTYPE: ExtractType.studentAssessment,
                             Constants.ASMTSUBJECT: param[Constants.ASMTSUBJECT],
                             Constants.ASMTTYPE: param[Constants.ASMTTYPE],
                             Constants.ASMTYEAR: param[Constants.ASMTYEAR],
                             Extract.REQUESTID: request_id}

            # separate by grades if no grade is specified
            __tasks, __task_responses = _create_tasks_with_responses(request_id, user, tenant, param, task_response, is_tenant_level=is_tenant_level)
            tasks += __tasks
            task_responses += __task_responses

    response['tasks'] = task_responses

    if len(tasks) > 0:
        archive_file_name = processor.get_archive_file_path(user.get_uid(), tenant, request_id)
        response['fileName'] = os.path.basename(archive_file_name)
        directory_to_archive = processor.get_extract_work_zone_path(tenant, request_id)

        # Register extract file with HPZ.
        registration_id, download_url = register_file(user.get_uid())
        response['download_url'] = download_url

        start_extract.apply_async(args=[tenant, request_id, archive_file_name, directory_to_archive, registration_id, tasks], queue=queue)  # @UndefinedVariable

    return response


def process_sync_item_or_raw_extract_request(params, extract_type):
    '''
    TODO add doc string
    '''
    settings = get_current_registry().settings
    queue = settings.get('extract.job.queue.sync', TaskConstants.SYNC_QUEUE_NAME)
    archive_queue = settings.get('extract.job.queue.archive', TaskConstants.ARCHIVE_QUEUE_NAME)
    data_path_config_key = 'extract.item_level_base_dir' if extract_type is ExtractType.itemLevel else 'extract.raw_data_base_dir'
    default_path = '/opt/edware/item_level' if extract_type is ExtractType.itemLevel else '/opt/edware/raw_data'
    root_dir = get_current_registry().settings.get(data_path_config_key, default_path)
    request_id, user, tenant = processor.get_extract_request_user_info()
    extract_params = copy.deepcopy(params)
    directory_to_archive = processor.get_extract_work_zone_path(tenant, request_id)
    out_file_name = get_items_extract_file_path(extract_params, tenant, request_id) if extract_type is ExtractType.itemLevel else None
    tasks, task_responses = _create_item_or_raw_tasks_with_responses(request_id, user, extract_params,
                                                                     root_dir, out_file_name, directory_to_archive,
                                                                     extract_type)
    if tasks:
        celery_timeout = int(get_current_registry().settings.get('extract.celery_timeout', '30'))
        prepare_path.apply_async(args=[request_id, [directory_to_archive]], queue=queue, immutable=True).get(timeout=celery_timeout)      # @UndefinedVariable
        generate_extract_file_tasks(tenant, request_id, tasks, queue_name=queue)().get(timeout=celery_timeout)
        result = archive_with_stream.apply_async(args=[request_id, directory_to_archive], queue=archive_queue, immutable=True)
        return result.get(timeout=celery_timeout)
    else:
        raise NotFoundException("There are no results")


def process_async_item_or_raw_extraction_request(params, extract_type):
    '''
    :param dict params: contains query parameter.  Value for each pair is expected to be a list
    :param bool is_tenant_level:  True if it is a tenant level request
    '''
    queue = get_current_registry().settings.get('extract.job.queue.async', TaskConstants.DEFAULT_QUEUE_NAME)
    data_path_config_key = 'extract.item_level_base_dir' if extract_type is ExtractType.itemLevel else 'extract.raw_data_base_dir'
    default_path = '/opt/edware/item_level' if extract_type is ExtractType.itemLevel else '/opt/edware/raw_data'
    root_dir = get_current_registry().settings.get(data_path_config_key, default_path)
    response = {}
    state_code = params[Constants.STATECODE]
    request_id, user, tenant = processor.get_extract_request_user_info(state_code)
    extract_params = copy.deepcopy(params)
    directory_to_archive = processor.get_extract_work_zone_path(tenant, request_id)
    out_file_name = get_items_extract_file_path(extract_params, tenant, request_id) if extract_type is ExtractType.itemLevel else None
    tasks, task_responses = _create_item_or_raw_tasks_with_responses(request_id, user, extract_params,
                                                                     root_dir, out_file_name, directory_to_archive,
                                                                     extract_type)

    response['tasks'] = task_responses
    if len(tasks) > 0:
        archive_file_name = processor.get_archive_file_path(user.get_uid(), tenant, request_id)
        response['fileName'] = os.path.basename(archive_file_name)

        # Register extract file with HPZ.
        registration_id, download_url = register_file(user.get_uid())
        response['download_url'] = download_url

        start_extract.apply_async(args=[tenant, request_id, archive_file_name, directory_to_archive, registration_id, tasks], queue=queue)  # @UndefinedVariable

    return response


def _get_asmt_records(state_code, district_guid, school_guid, asmt_grade, asmt_year, asmt_type, asmt_subject):
    '''
    query all asmt_guid and asmt_grade by given extract request params
    '''
    # TODO: remove dim_asmt
    with EdCoreDBConnection(state_code=state_code) as connector:
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        query = select_with_context([dim_asmt.c.asmt_guid.label(Constants.ASMT_GUID),
                                     fact_asmt_outcome_vw.c.asmt_grade.label(Constants.ASMT_GRADE)],
                                    from_obj=[dim_asmt
                                              .join(fact_asmt_outcome_vw, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id))], permission=RolesConstants.SAR_EXTRACTS, state_code=state_code)\
            .where(and_(fact_asmt_outcome_vw.c.state_code == state_code))\
            .where(and_(fact_asmt_outcome_vw.c.asmt_type == asmt_type))\
            .where(and_(fact_asmt_outcome_vw.c.asmt_subject == asmt_subject))\
            .where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT))\
            .group_by(dim_asmt.c.asmt_guid, fact_asmt_outcome_vw.c.asmt_grade)

        if district_guid is not None:
            query = query.where(and_(fact_asmt_outcome_vw.c.district_guid == district_guid))
        if school_guid is not None:
            query = query.where(and_(fact_asmt_outcome_vw.c.school_guid == school_guid))
        if asmt_grade is not None:
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == asmt_grade))
        if asmt_year is not None:
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_year == asmt_year))

        results = connector.get_result(query)
    return results


def _prepare_data(param):
    '''
    Prepare record for available pre-query extract
    '''
    asmt_guid_with_grades = []
    dim_asmt = None
    fact_asmt_outcome_vw = None
    asmt_type = param.get(Constants.ASMTTYPE)
    asmt_subject = param.get(Constants.ASMTSUBJECT)
    state_code = param.get(Constants.STATECODE)
    district_guid = param.get(Constants.DISTRICTGUID)
    school_guid = param.get(Constants.SCHOOLGUID)
    asmt_grade = param.get(Constants.ASMTGRADE)
    asmt_year = param.get(Constants.ASMTYEAR)
    available_records = _get_asmt_records(state_code, district_guid, school_guid, asmt_grade, asmt_year, asmt_type, asmt_subject)
    # Format to a list with a tuple of asmt_guid and grades
    for record_by_asmt_type in available_records:
        asmt_guid_with_grades.append((record_by_asmt_type[Constants.ASMT_GUID], record_by_asmt_type[Constants.ASMT_GRADE]))

    if asmt_guid_with_grades:
        with EdCoreDBConnection(state_code=state_code) as connector:
            dim_asmt = connector.get_table(Constants.DIM_ASMT)
            fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
    # Returns list of asmt guid with grades, and table objects
    return asmt_guid_with_grades, dim_asmt, fact_asmt_outcome_vw


def _create_tasks_with_responses(request_id, user, tenant, param, task_response={}, is_tenant_level=False):
    '''
    TODO comment
    '''
    tasks = []
    task_responses = []
    copied_task_response = copy.deepcopy(task_response)
    guid_grade, dim_asmt, fact_asmt_outcome_vw = _prepare_data(param)

    copied_params = copy.deepcopy(param)
    copied_params[Constants.ASMTGRADE] = None
    query = get_extract_assessment_query(copied_params)
    if guid_grade:
        for asmt_guid, asmt_grade in guid_grade:
            copied_params = copy.deepcopy(param)
            copied_params[Constants.ASMTGUID] = asmt_guid
            copied_params[Constants.ASMTGRADE] = asmt_grade
            query_with_asmt_rec_id_and_asmt_grade = query.where(and_(dim_asmt.c.asmt_guid == asmt_guid))\
                .where(and_(fact_asmt_outcome_vw.c.asmt_grade == asmt_grade))
            tasks += (_create_tasks(request_id, user, tenant, copied_params, query_with_asmt_rec_id_and_asmt_grade,
                                    is_tenant_level=is_tenant_level))
        copied_task_response[Extract.STATUS] = Extract.OK
        task_responses.append(copied_task_response)
    else:
        copied_task_response[Extract.STATUS] = Extract.FAIL
        copied_task_response[Extract.MESSAGE] = "Data is not available"
        task_responses.append(copied_task_response)
    return tasks, task_responses


def _create_item_or_raw_tasks_with_responses(request_id, user, param, root_dir, out_file, directory_to_archive,
                                             extract_type, task_response={}, is_tenant_level=False):
    '''
    TODO comment
    '''
    tasks = []
    task_responses = []
    copied_task_response = copy.deepcopy(task_response)
    states_to_tenants = get_state_code_to_tenant_map()
    guid_grade, _, _ = _prepare_data(param)

    if guid_grade:
        state_code = param.get(Constants.STATECODE)
        query = get_extract_assessment_item_and_raw_query(param)
        tenant = states_to_tenants[state_code]
        task = _create_new_task(request_id, user, tenant, param, query,
                                is_tenant_level=is_tenant_level, extract_type=extract_type)
        task[TaskConstants.TASK_FILE_NAME] = out_file
        task[TaskConstants.ROOT_DIRECTORY] = root_dir
        task[TaskConstants.DIRECTORY_TO_ARCHIVE] = directory_to_archive
        if extract_type is ExtractType.itemLevel:
            task[TaskConstants.ITEM_IDS] = param.get(Constants.ITEMID) if Constants.ITEMID in param else None
        tasks.append(task)
        copied_task_response[Extract.STATUS] = Extract.OK
        task_responses.append(copied_task_response)
    else:
        copied_task_response[Extract.STATUS] = Extract.FAIL
        copied_task_response[Extract.MESSAGE] = "Data is not available"
        task_responses.append(copied_task_response)
    return tasks, task_responses


def _create_tasks(request_id, user, tenant, params, query, is_tenant_level=False):
    '''
    TODO comment
    '''
    tasks = []
    tasks.append(_create_new_task(request_id, user, tenant, params, query, is_tenant_level=is_tenant_level,
                                  extract_file_path=get_extract_file_path))
    tasks.append(_create_asmt_metadata_task(request_id, user, tenant, params))
    return tasks


def _create_asmt_metadata_task(request_id, user, tenant, params):
    '''
    TODO comment
    '''
    query = get_asmt_metadata(params.get(Constants.STATECODE), params.get(Constants.ASMTGUID))
    return _create_new_task(request_id, user, tenant, params, query, asmt_metadata=True)


def _create_new_task(request_id, user, tenant, params, query, extract_type=None, asmt_metadata=False, is_tenant_level=False,
                     extract_file_path=None):
    '''
    TODO comment
    '''
    task = {}
    task[TaskConstants.TASK_TASK_ID] = create_new_entry(user, request_id, params)
    task[TaskConstants.TASK_QUERIES] = {QueryType.QUERY: compile_query_to_sql_text(query)}
    if asmt_metadata:
        task[TaskConstants.TASK_FILE_NAME] = get_asmt_metadata_file_path(params, tenant, request_id)
        task[TaskConstants.EXTRACTION_DATA_TYPE] = ExtractionDataType.QUERY_JSON
    else:
        if extract_file_path is not None:
            task[TaskConstants.TASK_FILE_NAME] = extract_file_path(params, tenant, request_id,
                                                                   is_tenant_level=is_tenant_level)
        if extract_type and extract_type is ExtractType.itemLevel:
            task[TaskConstants.EXTRACTION_DATA_TYPE] = ExtractionDataType.QUERY_ITEMS_CSV
        elif extract_type and extract_type is ExtractType.rawData:
            task[TaskConstants.EXTRACTION_DATA_TYPE] = ExtractionDataType.QUERY_RAW_XML
        else:
            task[TaskConstants.EXTRACTION_DATA_TYPE] = ExtractionDataType.QUERY_CSV
    return task


def get_extract_file_path(param, tenant, request_id, is_tenant_level=False):
    identifier = '_' + param.get(Constants.STATECODE) if is_tenant_level else ''
    file_name = 'ASMT_{asmtYear}{identifier}_{asmtGrade}_{asmtSubject}_{asmtType}_{currentTime}_{asmtGuid}.csv'.\
                format(identifier=identifier,
                       asmtGrade=('GRADE_' + param.get(Constants.ASMTGRADE)).upper(),
                       asmtSubject=param[Constants.ASMTSUBJECT].upper(),
                       asmtType=param[Constants.ASMTTYPE].upper(),
                       currentTime=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")),
                       asmtYear=param[Constants.ASMTYEAR],
                       asmtGuid=param[Constants.ASMTGUID])
    return os.path.join(processor.get_extract_work_zone_path(tenant, request_id), file_name)


def get_items_extract_file_path(param, tenant, request_id):
    file_name = '{prefix}_{stateCode}_{asmtYear}_{asmtType}_{asmtSubject}_GRADE_{asmtGrade}_{currentTime}.csv'.\
                format(prefix='ITEMS',
                       stateCode=param[Constants.STATECODE],
                       asmtYear=param[Constants.ASMTYEAR],
                       asmtType=param[Constants.ASMTTYPE].upper(),
                       asmtSubject=param[Constants.ASMTSUBJECT].upper(),
                       asmtGrade=param.get(Constants.ASMTGRADE),
                       currentTime=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")))
    return os.path.join(processor.get_extract_work_zone_path(tenant, request_id), file_name)


def get_asmt_metadata_file_path(params, tenant, request_id):
    return os.path.join(processor.get_extract_work_zone_path(tenant, request_id), get_metadata_file_name(params))
