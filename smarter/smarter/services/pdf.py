'''
Created on May 17, 2013

@author: dip
'''
from services.tasks.pdf import prepare, pdf_merge, get, archive, hpz_upload_cleanup
from urllib.parse import urljoin
from pyramid.view import view_config
from pyramid.response import Response
from smarter.security.context import check_context
from edapi.exceptions import InvalidParameterError, ForbiddenError
from edauth.security.utils import get_session_cookie
import urllib.parse
from sqlalchemy.sql import and_, select
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.security.context import select_with_context
from smarter.reports.helpers.filters import apply_filter_to_query
from edapi.httpexceptions import EdApiHTTPPreconditionFailed, \
    EdApiHTTPForbiddenAccess, EdApiHTTPInternalServerError, EdApiHTTPNotFound
from services.exceptions import PdfGenerationError
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from smarter.reports.helpers.constants import AssessmentType, Constants
from smarter.reports.helpers.filters import FILTERS_CONFIG
import services.celery
from edapi.decorators import validate_params
from edcore.utils.utils import to_bool, merge_dict
from hpz_client.frs.file_registration import register_file
from celery.canvas import group, chain
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
import copy
from datetime import datetime
import json
import os
from smarter_common.security.constants import RolesConstants
import pyramid

KNOWN_REPORTS = ['indivstudentreport.html']

PDF_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": merge_dict({
        Constants.STATECODE: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z]{2}$"},
        Constants.STUDENTGUID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False},
        Constants.DISTRICTGUID: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        Constants.SCHOOLGUID: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        Constants.ASMTGRADE: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[0-9]{0,2}$"
            },
            "minitems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.ASMTTYPE: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9 ]{0,50}$",
        },
        Constants.GRAYSCALE: {
            "type": "string",
            "required": False,
            "pattern": "^(true|false|TRUE|FALSE)$",
        },
        Constants.LANG: {
            "type": "string",
            "required": False,
            "pattern": "^[a-z]{2}$",
        },
        Constants.PDF: {
            "type": "string",
            "required": False,
            "pattern": "^(true|false|TRUE|FALSE)$",
        },
        Constants.SL: {
            "type": "string",
            "required": False,
            "pattern": "^\d+$",
        },
        Constants.EFFECTIVEDATE: {
            "type": "integer",
            "required": True,
            "pattern": "^[1-9]{8}$"
        },
        Constants.GROUP1ID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$"
            },
            "minitems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.GROUP2ID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$"
            },
            "minitems": 1,
            "uniqueItems": True,
            "required": False
        }
    }, FILTERS_CONFIG)
}


@view_config(route_name='pdf', request_method='POST', content_type='application/json')
@validate_params(schema=PDF_PARAMS)
def post_pdf_service(context, request):
    '''
    Handles POST request to /services/pdf

    :param request:  Pyramid request object
    '''
    try:
        params = request.json_body
    except ValueError:
        raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')

    return send_pdf_request(params)


@view_config(route_name='pdf', request_method='GET')
@validate_params(schema=PDF_PARAMS)
def get_pdf_service(context, request):
    '''
    Handles GET request to /services/pdf

    :param request:  Pyramid request object
    '''
    return send_pdf_request(request.GET)


def send_pdf_request(params):
    '''
    Requests for pdf content, throws http exceptions when error occurs

    :param params: python dict that contains query parameters from the request
    '''
    # Validate report type
    report = pyramid.threadlocal.get_current_request().matchdict['report'].lower()
    if report not in KNOWN_REPORTS:
        raise EdApiHTTPNotFound("Not Found")

    try:
        response = get_pdf_content(params)
    except InvalidParameterError as e:
        raise EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        raise EdApiHTTPForbiddenAccess(e.msg)
    except (PdfGenerationError, TimeoutError) as e:
        raise EdApiHTTPInternalServerError(e.msg)
    except Exception:
        # if celery get task got timed out...
        raise EdApiHTTPInternalServerError("Internal Error")

    return response


def get_pdf_content(params):
    # Collect the parameters
    student_guids = params.get(Constants.STUDENTGUID)
    state_code = params.get(Constants.STATECODE)
    district_guid = params.get(Constants.DISTRICTGUID)
    school_guid = params.get(Constants.SCHOOLGUID)
    grades = params.get(Constants.ASMTGRADE, [])
    asmt_type = params.get(Constants.ASMTTYPE, AssessmentType.SUMMATIVE)
    effective_date = str(params.get(Constants.EFFECTIVEDATE))
    is_grayscale = bool(params.get('grayscale', 'false').lower() == 'true')
    lang = params.get('lang', 'en').lower()
    subprocess_timeout = services.celery.TIMEOUT

    # Check that we have either a list of student GUIDs or a district/school/grade combination in the params
    if student_guids is None and (district_guid is None or school_guid is None or grades is None):
        raise InvalidParameterError('Required parameter is missing')
    # Validate the assessment type
    asmt_type = asmt_type.upper()
    if asmt_type not in [AssessmentType.SUMMATIVE, AssessmentType.INTERIM_COMPREHENSIVE]:
        raise InvalidParameterError('Unknown assessment type')

    # Get cookies and other config items
    (cookie_name, cookie_value) = get_session_cookie()
    celery_timeout = int(pyramid.threadlocal.get_current_registry().settings.get('pdf.celery_timeout', '30'))
    always_generate = to_bool(pyramid.threadlocal.get_current_registry().settings.get('pdf.always_generate', False))

    report = pyramid.threadlocal.get_current_request().matchdict['report']
    base_url = urljoin(pyramid.threadlocal.get_current_request().application_url, '/assets/html/' + report)
    # Set up a few additional variables
    pdf_base_dir = pyramid.threadlocal.get_current_registry().settings.get('pdf.report_base_dir', "/tmp")
    if student_guids is not None and type(student_guids) is not list:
        student_guids = [student_guids]

    if student_guids is not None and len(student_guids) is 1:
        response = get_single_pdf_content(pdf_base_dir, base_url, cookie_value, cookie_name, subprocess_timeout, state_code, effective_date, asmt_type, student_guids[0], lang, is_grayscale, always_generate, celery_timeout, params)
    else:
        response = get_bulk_pdf_content(pdf_base_dir, base_url, cookie_value, cookie_name, subprocess_timeout, student_guids, grades, state_code, district_guid, school_guid, asmt_type, effective_date, lang, is_grayscale, always_generate, celery_timeout, params)
    return response


def get_single_pdf_content(pdf_base_dir, base_url, cookie_value, cookie_name, subprocess_timeout, state_code, effective_date, asmt_type, student_guid, lang, is_grayscale, always_generate, celery_timeout, params):
    # Get all file names
    url = _create_student_pdf_url(student_guid, base_url, params)
    files_by_guid = generate_isr_report_path_by_student_guid(state_code, effective_date,
                                                             pdf_report_base_dir=pdf_base_dir, student_guids=[student_guid],
                                                             asmt_type=asmt_type, grayScale=is_grayscale, lang=lang)
    file_name = files_by_guid[student_guid]
    celery_response = get.delay(cookie_value, url, file_name, cookie_name=cookie_name, timeout=subprocess_timeout, grayscale=is_grayscale, always_generate=always_generate)  # @UndefinedVariable
    pdf_stream = celery_response.get(timeout=celery_timeout)

    return Response(body=pdf_stream, content_type='application/pdf')


def get_bulk_pdf_content(pdf_base_dir, base_url, cookie_value, cookie_name, subprocess_timeout, student_guids, grades,
                         state_code, district_guid, school_guid, asmt_type, effective_date, lang, is_grayscale,
                         always_generate, celery_timeout, params):
    '''
    Read pdf content from file system if it exists, else generate it

    :param params: python dict that contains query parameters from the request
    '''
    # Get the user
    user = authenticated_userid(get_current_request())

    # If we do not have a list of student GUIDs, we need to get it
    all_guids, guids_by_grade = _create_student_guids(student_guids, grades, state_code, district_guid, school_guid,
                                                      asmt_type, effective_date, params)

    # Get all file names
    files_by_student_guid = generate_isr_report_path_by_student_guid(state_code, effective_date,
                                                                     pdf_report_base_dir=pdf_base_dir,
                                                                     student_guids=all_guids, asmt_type=asmt_type,
                                                                     grayScale=is_grayscale, lang=lang)

    # Set up a few additional variables
    urls_by_student_guid = _create_urls_by_student_guid(all_guids, state_code, base_url, params)

    # Register expected file with HPZ
    registration_id, download_url = register_file(user.get_uid())

    # Get the name of the school
    school_name = _get_school_name(state_code, district_guid, school_guid)

    # Set up directory and file names
    directory_to_archive = os.path.join(pdf_base_dir, 'bulk', registration_id, 'data')
    directory_for_zip = os.path.join(pdf_base_dir, 'bulk', registration_id, 'zip')
    archive_file_name = _get_archive_name(school_name, lang, is_grayscale)
    archive_file_path = os.path.join(directory_for_zip, archive_file_name)

    # Create JSON response
    response = {'fileName': archive_file_name, 'download_url': download_url}

    # Create the tasks for each individual student PDF file we want to merge
    generate_tasks = _create_pdf_generate_tasks(cookie_value, cookie_name, is_grayscale, always_generate, files_by_student_guid,
                                                urls_by_student_guid)

    # Create the tasks to merge each PDF by grade
    merge_tasks = _create_pdf_merge_tasks(pdf_base_dir, directory_to_archive, guids_by_grade, files_by_student_guid,
                                          school_name, lang, is_grayscale)

    # Start the bulk merge
    _start_bulk(archive_file_path, directory_to_archive, registration_id, generate_tasks, merge_tasks, pdf_base_dir)

    # Return the JSON response while the bulk merge runs asynchronously
    return Response(body=json.dumps(response), content_type='application/json')


def _create_student_guids(student_guids, grades, state_code, district_guid, school_guid, asmt_type, effective_date, params):
    '''
    create list of student guids by grades
    '''
    # If we do not have a list of student GUIDs, we need to get it
    all_guids = []
    guids_by_grade = {}
    if student_guids is None:
        for grade in grades:
            guids = _get_student_guids(state_code, district_guid, school_guid, grade, asmt_type, effective_date, params)
            if len(guids) > 0:
                all_guids.extend([result[Constants.STUDENT_GUID] for result in guids])
                guids_by_grade[grade] = [result[Constants.STUDENT_GUID] for result in guids]
    else:
        all_guids.extend(student_guids)
        guids_by_grade['all'] = student_guids
    if len(all_guids) == 0:
        raise InvalidParameterError('No students match filters')
    return all_guids, guids_by_grade


def _create_urls_by_student_guid(all_guids, state_code, base_url, params):
    '''
    create ISR URL link for each students
    '''
    # Set up a few additional variables
    urls_by_guid = {}

    # Check if the user has access to PII for all of these students
    if not _has_context_for_pdf_request(state_code, all_guids):
        raise ForbiddenError('Access Denied')
    # Create URLs
    for student_guid in all_guids:
        urls_by_guid[student_guid] = _create_student_pdf_url(student_guid, base_url, params)
    return urls_by_guid


def _create_pdf_generate_tasks(cookie_value, cookie_name, is_grayscale, always_generate, files_by_guid, urls_by_guid):
    '''
    create celery tasks to prepare pdf files.
    '''
    generate_tasks = []
    args = {'cookie': cookie_value, 'timeout': services.celery.TIMEOUT, 'cookie_name': cookie_name,
            'grayscale': is_grayscale, 'always_generate': always_generate}
    for student_guid, file_name in files_by_guid.items():
        copied_args = copy.deepcopy(args)
        copied_args['url'] = urls_by_guid[student_guid]
        copied_args['outputfile'] = file_name
        generate_tasks.append(prepare.subtask(kwargs=copied_args, immutable=True))  # @UndefinedVariable
    return generate_tasks


def _create_pdf_merge_tasks(pdf_base_dir, directory_to_archive, guids_by_grade, files_by_guid, school_name, lang,
                            is_grayscale):
    '''
    create pdf merge tasks
    '''
    merge_tasks = []
    for grade, student_guids in guids_by_grade.items():
        # Create bulk output name and path
        bulk_name = _get_merged_pdf_name(school_name, grade, lang, is_grayscale)
        bulk_path = os.path.join(directory_to_archive, bulk_name)

        # Get the files for this grade
        file_names = []
        for student_guid in student_guids:
            file_names.append(files_by_guid[student_guid])

        # Create the merge task
        merge_tasks.append(pdf_merge.subtask(args=(file_names, bulk_path, pdf_base_dir, services.celery.TIMEOUT), immutable=True))  # @UndefinedVariable
    return merge_tasks


def _has_context_for_pdf_request(state_code, student_guid):
    '''
    Validates that user has context to student_guid

    :param student_guid:  guid(s) of the student(s)
    '''
    if type(student_guid) is not list:
        student_guid = [student_guid]
    return check_context(RolesConstants.PII, state_code, student_guid)


def _create_student_pdf_url(student_guid, base_url, params):
    params[Constants.STUDENTGUID] = student_guid
    encoded_params = urllib.parse.urlencode(params)
    return base_url + "?%s" % encoded_params


def _start_bulk(archive_file_path, directory_to_archive, registration_id, gen_tasks, merge_tasks, pdf_base_dir):
    '''
    entry point to start a bulk PDF generation request for one or more students
    it groups the generation of individual PDFs into a celery task group and then chains it to the next task to merge
    the files into one PDF, archive the PDF into a zip, and upload the zip to HPZ
    '''

    workflow = chain(group(gen_tasks),
                     group(merge_tasks),
                     archive.subtask(args=(archive_file_path, directory_to_archive), immutable=True),  # @UndefinedVariable
                     hpz_upload_cleanup.subtask(args=(archive_file_path, registration_id, pdf_base_dir), immutable=True))  # @UndefinedVariable
    workflow.apply_async()


def _get_merged_pdf_name(school_name, grade, lang_code, grayscale):
    timestamp = str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
    school_name = school_name.replace(' ', '')
    school_name = school_name[:15] if len(school_name) > 15 else school_name
    grade_val = '_grade_{grade}'.format(grade=grade) if grade != 'all' else ''
    name = 'student_reports_{school_name}{grade}_{timestamp}_{lang}'.format(school_name=school_name,
                                                                            grade=grade_val,
                                                                            timestamp=timestamp,
                                                                            lang=lang_code.lower())
    return name + ('.g.pdf' if grayscale else '.pdf')


def _get_archive_name(school_name, lang_code, grayscale):
    timestamp = str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
    school_name = school_name.replace(' ', '')
    school_name = school_name[:15] if len(school_name) > 15 else school_name
    name = 'student_reports_{school_name}_{timestamp}_{lang}'.format(school_name=school_name,
                                                                     timestamp=timestamp,
                                                                     lang=lang_code.lower())
    return name + ('.g.zip' if grayscale else '.zip')


def _get_student_guids(state_code, district_guid, school_guid, grade, asmt_type, effective_date, params):
    with EdCoreDBConnection(state_code=state_code) as connector:
        # Get handle to tables
        dim_student = connector.get_table(Constants.DIM_STUDENT)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)

        # Build select
        query = select_with_context([fact_asmt_outcome_vw.c.student_guid.label(Constants.STUDENT_GUID),
                                     dim_student.c.first_name,
                                     dim_student.c.last_name],
                                    from_obj=[fact_asmt_outcome_vw
                                              .join(dim_student, and_(fact_asmt_outcome_vw.c.student_rec_id == dim_student.c.student_rec_id))
                                              .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id))],
                                    permission=RolesConstants.PII, state_code=state_code).distinct()

        # Add where clauses
        query = query.where(fact_asmt_outcome_vw.c.state_code == state_code)
        query = query.where(and_(fact_asmt_outcome_vw.c.school_guid == school_guid))
        query = query.where(and_(fact_asmt_outcome_vw.c.district_guid == district_guid))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == grade))
        query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_type == asmt_type))
        query = query.where(and_(dim_asmt.c.effective_date == effective_date))
        query = apply_filter_to_query(query, fact_asmt_outcome_vw, params)

        # Check for group IDs
        if Constants.GROUP1ID in params:
            query = query.where(and_(fact_asmt_outcome_vw.c.group_1_id.in_(params.get(Constants.GROUP1ID))))
        if Constants.GROUP2ID in params:
            query = query.where(and_(fact_asmt_outcome_vw.c.group_2_id.in_(params.get(Constants.GROUP2ID))))

        # Add order by clause
        query = query.order_by(dim_student.c.last_name).order_by(dim_student.c.first_name)

        # Return the result
        return connector.get_result(query)


def _get_school_name(state_code, district_guid, school_guid):
    with EdCoreDBConnection(state_code=state_code) as connector:
        # Get handle to tables
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)

        # Build select
        query = select([dim_inst_hier.c.school_name.label(Constants.SCHOOL_NAME)],
                       from_obj=[dim_inst_hier])

        # Add where clauses
        query = query.where(dim_inst_hier.c.state_code == state_code)
        query = query.where(and_(dim_inst_hier.c.district_guid == district_guid))
        query = query.where(and_(dim_inst_hier.c.school_guid == school_guid))

        # Return the result
        return connector.get_result(query)[0][Constants.SCHOOL_NAME]
