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
from edapi.httpexceptions import EdApiHTTPPreconditionFailed, \
    EdApiHTTPInternalServerError
import json
from smarter.reports.helpers.constants import AssessmentType, Constants
from smarter.extracts.student_asmt_processor import process_extraction_request
from smarter.extracts.constants import ExtractType, Constants as Extract
from datetime import datetime
import logging
from smarter.reports.helpers.filters import FILTERS_CONFIG
from edcore.utils.utils import merge_dict

logger = logging.getLogger(__name__)

TENANT_EXTRACT_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": merge_dict({
        Extract.EXTRACTTYPE: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^" + ExtractType.studentAssessment + "$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.ASMTTYPE: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^(" + AssessmentType.SUMMATIVE + "|" + AssessmentType.INTERIM_COMPREHENSIVE + ")$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": True
        },
        Constants.ASMTSUBJECT: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^(" + Constants.MATH + "|" + Constants.ELA + ")$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": True
        },
        Constants.ASMTYEAR: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^\d{4}$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.STATECODE: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z]{2}$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": True,
        },
        Constants.DISTRICTGUID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$",
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.SCHOOLGUID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$",
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.ASMTGRADE: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$",
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
        },
        Constants.STUDENTGUID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]{0,50}$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
        },
        Extract.SYNC: {
            "type": "string",
            "required": False,
            "pattern": "^(true|TRUE)$",
        },
        Extract.ASYNC: {
            "type": "string",
            "required": False,
            "pattern": "^(true|TRUE)$",
        },
        Constants.SL: {  # this is added by GET request inside browsers
            "type": "string",
            "pattern": "^\d+$",
            "required": False
        }
    }, FILTERS_CONFIG)
}


@view_config(route_name='extract', request_method='POST')
@validate_params(schema=TENANT_EXTRACT_PARAMS)
@audit_event()
def post_extract_service(context, request):
    '''
    Handles POST request to /services/extract/school

    :param request:  Pyramid request object
    '''
    params = convert_query_string_to_dict_arrays(request.json_body)
    return send_extraction_request(params)


@view_config(route_name='extract', request_method='GET')
@validate_params(schema=TENANT_EXTRACT_PARAMS)
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

    Sync and Async type are both processed here
    Sync calls return content type of 'application/octet-stream'
    Async calls return a json Response

    By default, it is a synchronous call unless otherwise specified

    :param session: session for this user request
    :param params: python dict that contains query parameters from the request
    '''
    response = None
    try:
        # By default, it is a sync call
        is_async = params.get(Extract.ASYNC, False)
        results = process_extraction_request(params, is_async=is_async)
        if is_async:
            # TODO: we should validate the type when we refactor the endpoint
            # if ExtractType.studentAssessment in params[Extract.EXTRACTTYPE]:
            response = Response(body=json.dumps(results), content_type='application/json')
        else:
            zip_file_name = generate_zip_file_name(params.get(Constants.ASMTYEAR, [None])[0],
                                                   params.get(Constants.ASMTGRADE, [None]),
                                                   params.get(Constants.ASMTTYPE, [None])[0],
                                                   params.get(Constants.ASMTSUBJECT),)
            response = Response(body=results, content_type='application/octet-stream')
            response.headers['Content-Disposition'] = ("attachment; filename=\"%s\"" % zip_file_name)
    # TODO: currently we dont' even throw any of these exceptions
    except ExtractionError as e:
        raise EdApiHTTPInternalServerError(e.msg)
    except TimeoutError as e:
        # if celery timed out...
        raise EdApiHTTPInternalServerError(e.msg)
    except Exception as e:
        # uknown exception was thrown.  Most likely configuration issue.
        logger.error(str(e))
        raise
    return response


def generate_zip_file_name(asmt_year, asmt_grade, asmt_type, asmt_subject):
    '''
    Generate file name for archive file according
        Zip file name:

        School-level: ASMT_<subject>_<type>_<timestamp>.zip
        Grade-level:  ASMT_<grade>_<subject>_<type>_<timestamp>.zip
    '''
    asmt_subject.sort()
    asmtSubjects = '_'.join(asmt_subject)
    identifier = '_GRADE_' + str(asmt_grade[0]) if len(asmt_grade) == 1 and asmt_grade[0] is not None else ''
    return "ASMT_{asmtYear}{identifier}_{asmtSubject}_{asmtType}_{timestamp}.zip".\
        format(identifier=identifier,
               asmtSubject=asmtSubjects.upper(),
               asmtType=asmt_type.upper(),
               asmtYear=asmt_year,
               timestamp=datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
