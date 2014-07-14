import json
from pyramid.response import Response
from pyramid.view import view_config
from edapi.decorators import validate_params
from edapi.logging import audit_event
from edapi.utils import convert_query_string_to_dict_arrays
from smarter.extracts.student_reg_processor import process_extraction_request
from smarter.reports.helpers.constants import Constants
from smarter.extracts.constants import Constants as Extract, ExtractType

STUDENT_REGISTRATION_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        Extract.EXTRACTTYPE: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^(" + ExtractType.studentRegistrationStatistics + "|" + ExtractType.studentAssessmentCompletion + ")$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": True
        },
        Constants.ACADEMIC_YEAR: {
            "type": "array",
            "items": {
                "type": "integer",
                "pattern": "^\d{4}$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": True
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
        }
    }
}


@view_config(route_name='student_registration_statistics', request_method='POST')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def post_sr_stat_extract_service(context, request):
    '''
    Handles POST request to /services/extract/student_registration_statistic

    :param context:  Pyramid context object
    :param request:  Pyramid request object
    '''
    return process_extract(request)


@view_config(route_name='student_assessment_completion', request_method='POST')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def post_sa_comp_extract_service(context, request):
    '''
    Handles POST request to /services/extract/student_assessment_completion

    :param context:  Pyramid context object
    :param request:  Pyramid request object
    '''
    return process_extract(request)


def process_extract(request):
    params = convert_query_string_to_dict_arrays(request.json_body)
    results = process_extraction_request(params)
    return Response(body=json.dumps(results), content_type='application/json')
