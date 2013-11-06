'''
Created on Nov 1, 2013

@author: ejen
'''
from pyramid.view import view_config
from edapi.logging import audit_event
from edapi.decorators import validate_params
from edapi.exceptions import InvalidParameterError, ForbiddenError
from edextract.exceptions import ExtractionError
from pyramid.response import Response
from edapi.httpexceptions import EdApiHTTPPreconditionFailed,\
    EdApiHTTPForbiddenAccess, EdApiHTTPInternalServerError
import json
from edextract.tasks.smarter_query import process_extraction_request
from edauth.security.utils import get_session_cookie

EXTRACT_POST_PARAMS = {
    "type": "object",
    "properties": {
        'extractType': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^studentAssessment$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'asmtType': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^SUMMATIVE$|^INTERIM$"
            },
            "minItems": 1,
            "uniqueItems": True
        },
        'asmtSubject': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^Math$|^ELA$"
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
        'asmtState': {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[a-zA-Z]{2}$"
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["extractType", "asmtSubject", "asmtType", "asmtYear", "asmtState"]
}


@view_config(route_name='extract', request_method='POST', content_type='application/json')
@validate_params(method='POST', schema=EXTRACT_POST_PARAMS)
#@audit_event()
def post_extract_service(context, request):
    '''
    Handles POST request to /services/extract

    :param request:  Pyramid request object
    '''
    try:
        params = request.json_body
    except ValueError:
        raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')

    return send_extraction_request(params)


@view_config(route_name='extract', request_method='GET')
@validate_params(method='GET', schema=EXTRACT_POST_PARAMS)
#@audit_event()
def get_extract_service(context, request):
    '''
    Handles GET request to /services/extract

    :param request:  Pyramid request object
    '''
    # flatten the parameters
    query_string = request.GET
    params = {}
    for k in query_string.keys():
        params[k] = query_string.getall(k)
    return send_extraction_request(params)


def send_extraction_request(params):
    '''
    Requests for data extraction, throws http exceptions when error occurs

    :param params: python dict that contains query parameters from the request
    '''
    cookie = get_session_cookie()
    try:
        celery_result = process_extraction_request.delay(cookie, params)  # @UndefinedVariable
        task_responses = celery_result.get()
        return Response(body=json.dumps(task_responses), content_type='application/json')
    except InvalidParameterError as e:
        raise EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        raise EdApiHTTPForbiddenAccess(e.msg)
    except ExtractionError as e:
        raise EdApiHTTPInternalServerError(e.msg)
    except TimeoutError as e:
        # if celery get task got timed out...
        raise EdApiHTTPInternalServerError(e.msg)
