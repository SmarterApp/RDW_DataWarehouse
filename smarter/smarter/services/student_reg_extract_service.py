import json
from pyramid.response import Response
from pyramid.view import view_config
from edapi.decorators import validate_params
from edapi.logging import audit_event
from smarter.extracts.student_reg_processor import process_extraction_request
from smarter.reports.helpers.constants import Constants
from smarter.extracts.constants import Constants as Extract, ExtractType

STUDENT_REGISTRATION_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        Extract.EXTRACTTYPE: {
            "type": "string",
            "pattern": "^(" + ExtractType.studentRegistrationStatistics + "|" + ExtractType.studentAssessmentCompletion + ")$",
            "required": False
        },
        Constants.ACADEMIC_YEAR: {
            "type": "integer",
            "pattern": "^\d{4}$",
            "required": True
        },
        Constants.STATECODE: {
            "type": "string",
            "pattern": "^[a-zA-Z]{2}$",
            "required": True,
        }
    }
}


@view_config(route_name='student_registration_statistics')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def post_sr_stat_extract_service(context, request):
    '''
    Handles POST request to /services/extract/student_registration_statistic

    :param context:  Pyramid context object
    :param request:  Pyramid request object
    '''
    params = request.validated_params.copy()
    params[Extract.EXTRACTTYPE] = ExtractType.studentRegistrationStatistics
    return process_extract(params)


@view_config(route_name='student_assessment_completion', request_method='POST')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def post_sa_comp_extract_service(context, request):
    '''
    Handles POST request to /services/extract/student_assessment_completion

    :param context:  Pyramid context object
    :param request:  Pyramid request object
    '''
    params = request.validated_params.copy()
    params[Extract.EXTRACTTYPE] = ExtractType.studentAssessmentCompletion
    return process_extract(params)


def process_extract(params):
    fixed_params = {}
    for k, v in params.items():
        fixed_params[k] = v
    results = process_extraction_request(fixed_params)
    return Response(body=json.dumps(results), content_type='application/json')
