'''
Created on May 2, 2014

@author: nestep
'''
from pyramid.view import view_config
from edapi.logging import audit_event
from edapi.decorators import validate_params
from edapi.utils import convert_query_string_to_dict_arrays
from edextract.exceptions import ExtractionError
from edcore.utils.utils import merge_dict
from pyramid.response import Response
from edapi.httpexceptions import EdApiHTTPPreconditionFailed,\
    EdApiHTTPInternalServerError
import json
from smarter.reports.helpers.constants import AssessmentType, Constants
from smarter.extracts.student_asmt_processor import process_async_item_extraction_request,\
    process_sync_item_extract_request
from smarter.extracts.constants import ExtractType, Constants as Extract
from smarter.reports.helpers.filters import FILTERS_CONFIG
from datetime import datetime
import logging
import copy

logger = logging.getLogger(__name__)

ITEM_EXTRACT_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": merge_dict({
        Extract.EXTRACTTYPE: {
            "type": "string",
            "pattern": "^" + ExtractType.itemLevel + "$",
            "required": True
        },
        Constants.STATECODE: {
            "type": "string",
            "pattern": "^[a-zA-Z]{2}$",
            "required": True
        },
        Constants.ASMTYEAR: {
            "type": "string",
            "pattern": "^\d{4}$",
            "required": True
        },
        Constants.ASMTTYPE: {
            "type": "string",
            "pattern": "^(" + AssessmentType.SUMMATIVE + "|" + AssessmentType.INTERIM_COMPREHENSIVE + ")$",
            "required": True
        },
        Constants.ASMTSUBJECT: {
            "type": "string",
            "pattern": "^(" + Constants.MATH + "|" + Constants.ELA + ")$",
            "required": True
        },
        Constants.ASMTGRADE: {
            "type": "string",
            "pattern": "^[K0-9]+$",
            "maxLength": 2,
            "required": True,
        },
        Constants.ITEMID: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9\-]*$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False,
        },
        Extract.ASYNC: {
            "type": "string",
            "required": False,
            "pattern": "^(true|TRUE)$",
        },
        Extract.SYNC: {
            "type": "string",
            "required": False,
            "pattern": "^(true|TRUE)$",
        }
    }, FILTERS_CONFIG)
}


@view_config(route_name='assessment_item_level', request_method='POST')
@validate_params(schema=ITEM_EXTRACT_PARAMS)
@audit_event()
def post_item_extract_service(context, request):
    '''
    Handles POST request to /services/extract/assessment_item_level

    :param request:  Pyramid request object
    '''
    params = {}
    for k, v in request.json_body.items():
        params[k] = v
    return send_extraction_request(params)


@view_config(route_name='assessment_item_level', request_method='GET')
@validate_params(schema=ITEM_EXTRACT_PARAMS)
@audit_event()
def get_item_extract_service(context, request):
    '''
    Handles GET request to /services/extract/assessment_item_level

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
        if is_async:
            results = process_async_item_extraction_request(params)
            response = Response(body=json.dumps(results), content_type='application/json')
        else:
            extract_params = copy.deepcopy(params)
            zip_file_name = generate_zip_file_name(extract_params)
            content = process_sync_item_extract_request(extract_params)
            response = Response(body=content, content_type='application/octet-stream')
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


def generate_zip_file_name(params):
    '''
    Generate file name for archive file according
        Zip file name:

        ITEMS_<year>_<type>_<subject>_<grade>_<timestamp>.zip
    '''
    return "ITEMS_{asmtYear}_{asmtType}_{asmtSubject}_{asmtGrade}_{timestamp}.zip".\
        format(asmtYear=params.get(Constants.ASMTYEAR),
               asmtType=params.get(Constants.ASMTTYPE).upper(),
               asmtSubject=params.get(Constants.ASMTSUBJECT).upper(),
               asmtGrade=params.get(Constants.ASMTGRADE).upper(),
               timestamp=datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
