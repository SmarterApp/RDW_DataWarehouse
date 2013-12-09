'''
Created on Nov 1, 2013

@author: ejen
'''
from pyramid.view import view_config
from edapi.logging import audit_event
from edapi.decorators import validate_params
from edapi.utils import convert_query_string_to_dict_arrays
from edextract.exceptions import ExtractionError
from pyramid.response import Response
from edapi.httpexceptions import EdApiHTTPPreconditionFailed,\
    EdApiHTTPInternalServerError
import json
from smarter.reports.helpers.constants import AssessmentType, Constants
from smarter.extract.processor import process_async_extraction_request,\
    process_sync_extract_request
from smarter.extract.constants import ExtractType, Constants as Extract
from edcore.utils.utils import merge_dict
from smarter.reports.list_of_students_report import REPORT_PARAMS
from datetime import datetime

TENANT_EXTRACT_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        'extractType': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^" + ExtractType.studentAssessment + "$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'asmtType': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^(" + AssessmentType.SUMMATIVE + "|" + AssessmentType.COMPREHENSIVE_INTERIM + ")$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'asmtSubject': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^(" + Constants.MATH + "|" + Constants.ELA + ")$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'asmtYear': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^\d{4}$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'stateCode': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z]{2}$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'sl': {  # this is added by GET request inside browsers
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^\d+$"
            },
            "required": False
        }
    },
    "required": ["extractType", "asmtSubject", "asmtType", "asmtYear", "stateCode"]
}

EXTRACT_PARAMS = {"type": "object",
                  "additionalProperties": False,
                  "properties": merge_dict(REPORT_PARAMS,
                                           {Constants.ASMTTYPE: {"type": "string",
                                                                 "require": True,
                                                                 "pattern": "^(" + AssessmentType.SUMMATIVE + "|" + AssessmentType.COMPREHENSIVE_INTERIM + ")$"},
                                            'sl': {"type": "string",
                                                   "required": False}
                                            })}


@view_config(route_name='tenant_extract', request_method='POST', content_type='application/json')
@validate_params(schema=TENANT_EXTRACT_PARAMS)
@audit_event()
def post_tenant_level_extract_service(context, request):
    '''
    Handles POST request to /services/extract/tenant

    :param request:  Pyramid request object
    '''
    try:
        params = request.json_body
    except Exception as e:
        raise EdApiHTTPPreconditionFailed(e)
    return send_tenant_level_extraction_request(params)


@view_config(route_name='tenant_extract', request_method='GET')
@validate_params(schema=TENANT_EXTRACT_PARAMS)
@audit_event()
def get_tenant_level_extract_service(context, request):
    '''
    Handles GET request to /services/extract/tenant

    :param request:  Pyramid request object
    '''
    try:
        params = convert_query_string_to_dict_arrays(request.GET)
    except Exception as e:
        raise EdApiHTTPPreconditionFailed(e)
    return send_tenant_level_extraction_request(params)


def send_tenant_level_extraction_request(params):
    '''
    Requests for data extraction for tenant level, throws http exceptions when error occurs

    :param session: session for this user request
    :param params: python dict that contains query parameters from the request
    '''
    try:
        if ExtractType.studentAssessment in params[Extract.EXTRACTTYPE]:
            results = process_async_extraction_request(params)
            return Response(body=json.dumps(results), content_type='application/json')
    # TODO: currently we dont' even throw any of these exceptions
    except ExtractionError as e:
        raise EdApiHTTPInternalServerError(e.msg)
    except TimeoutError as e:
        # if celery timed out...
        raise EdApiHTTPInternalServerError(e.msg)


@view_config(route_name='extract', request_method='POST', content_type='application/octet-stream')
@validate_params(schema=EXTRACT_PARAMS)
@audit_event()
def post_extract_service(context, request):
    '''
    Handles POST request to /services/extract/school

    :param request:  Pyramid request object
    '''
    try:
        params = request.json_body
        for k, v in params.items():
            if type(v) is not list:
                params[k] = [v]
    except Exception as e:
        raise EdApiHTTPPreconditionFailed(e)
    return send_extraction_request(params)


@view_config(route_name='extract', request_method='GET')
@validate_params(schema=EXTRACT_PARAMS)
@audit_event()
def get_extract_service(context, request):
    '''
    Handles GET request to /services/extract/school

    :param request:  Pyramid request object
    '''
    try:
        params = convert_query_string_to_dict_arrays(request.GET)
    except Exception as e:
        raise EdApiHTTPPreconditionFailed(e)
    return send_extraction_request(params)


def send_extraction_request(params):
    '''
    Requests for data extraction

    :param session: session for this user request
    :param params: python dict that contains query parameters from the request
    '''
    extract_params = {Constants.STATECODE: params.get(Constants.STATECODE, [None])[0],
                      Constants.DISTRICTGUID: params.get(Constants.DISTRICTGUID, [None])[0],
                      Constants.SCHOOLGUID: params.get(Constants.SCHOOLGUID, [None])[0],
                      Constants.ASMTTYPE: params.get(Constants.ASMTTYPE, [None])[0],
                      Constants.ASMTGRADE: params.get(Constants.ASMTGRADE, [None])[0],
                      Constants.ASMTSUBJECT: params.get(Constants.ASMTSUBJECT)}
    zip_file_name = generate_zip_file_name(extract_params)
    content = process_sync_extract_request(extract_params)
    response = Response(body=content, content_type='application/octet-stream')
    response.headers['Content-Disposition'] = ("attachment; filename=\"%s\"" % zip_file_name)
    return response


def generate_zip_file_name(params):
    '''
    Generate file name for archive file according
        Zip file name:

        School-level: ASMT_<subject>_<type>_<timestamp>.zip
        Grade-level:  ASMT_<grade>_<subject>_<type>_<timestamp>.zip
    '''
    subjects = params.get(Constants.ASMTSUBJECT)
    subjects.sort()
    asmtSubjects = '_'.join(subjects)
    asmtGrade = params.get(Constants.ASMTGRADE)
    identifier = '_GRADE_' + str(asmtGrade) if asmtGrade is not None else ''
    return "ASMT{identifier}_{asmtSubject}_{asmtType}_{timestamp}.zip".format(identifier=identifier,
                                                                              asmtSubject=asmtSubjects.upper(),
                                                                              asmtType=params.get(Constants.ASMTTYPE).upper(),
                                                                              timestamp=datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
