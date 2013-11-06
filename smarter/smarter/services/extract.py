'''
Created on Nov 1, 2013

@author: ejen
'''
from pyramid.view import view_config
from edapi.logging import audit_event
from edapi.decorators import validate_params
from smarter.reports.extraction import get_check_ela_interim_assessment_existence_query,\
    get_check_math_interim_assessment_existence_query,\
    get_check_ela_summative_assessment_existence_query,\
    get_check_math_summative_assessment_existence_query,\
    get_ela_interim_assessment_query,\
    get_math_interim_assessment_query,\
    get_ela_summative_assessment_query,\
    get_math_summative_assessment_query
from pyramid.response import Response
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from smarter.reports.helpers.constants import Constants
import json
from edextract.tasks.query import handle_request
from celery.result import AsyncResult
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

EXTRACT_QUERY_MAP = {
    'studentAssessment_Math_INTERIM': (get_check_math_interim_assessment_existence_query,
                                       get_math_interim_assessment_query),
    'studentAssessment_ELA_INTERIM': (get_check_ela_interim_assessment_existence_query,
                                      get_ela_interim_assessment_query),
    'studentAssessment_Math_SUMMATIVE': (get_check_math_summative_assessment_existence_query,
                                         get_math_summative_assessment_query),
    'studentAssessment_ELA_SUMMATIVE': (get_check_ela_summative_assessment_existence_query,
                                        get_ela_summative_assessment_query)
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
    for k, v in query_string.items():
        if params.get(k) is None:
            params[k] = [v]
        else:
            params[k].append(v)
    return send_extraction_request(params)


def send_extraction_request(params):
    '''
    Requests for data extraction, throws http exceptions when error occurs

    :param params: python dict that contains query parameters from the request
    '''
    cookie = get_session_cookie()
    query_lookups = []
    for e in params['extractType']:
        for s in params['asmtSubject']:
            for t in params['asmtType']:
                query_lookups.append(e + '_' + s + '_' + t)
    tasks = []
    task_responses = []

    for l in query_lookups:
        query_calls = EXTRACT_QUERY_MAP[l]
        queries = []
        for q in query_calls:
            queries.append(q(params['asmtYear'][0]))
        tasks.append({'key': l, 'queries': queries})

    try:
        for task in tasks:
            celery_response = handle_request.delay(cookie=cookie, task_queries=task['queries'])
            task_id = celery_response.task_id
            key_parts = task['key'].split('_')
            task_responses.append({
                'status': Constants.OK,
                'id': task_id,
                'asmtYear': params['asmtYear'][0],
                'asmtState': params['asmtState'][0],
                'extractType': key_parts[0],
                'asmtSubject': key_parts[1],
                'asmtType': key_parts[2]
            })
        return Response(body=json.dumps(task_responses), content_type='application/json')
    except InvalidParameterError as e:
        raise EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        raise EdApiHTTPForbiddenAccess(e.msg)
    except PdfGenerationError as e:
        raise EdApiHTTPInternalServerError(e.msg)
    except TimeoutError as e:
        # if celery get task got timed out...
        raise EdApiHTTPInternalServerError(e.msg)
