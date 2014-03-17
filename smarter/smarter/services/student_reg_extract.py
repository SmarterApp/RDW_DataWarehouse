import json
from pyramid.response import Response
from pyramid.view import view_config
from edapi.decorators import validate_params
from edapi.logging import audit_event
from edapi.utils import convert_query_string_to_dict_arrays
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
                "pattern": "^" + ExtractType.studentRegistrationStatistics + "$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": False
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
        },
        Extract.ASYNC: {
            "type": "string",
            "required": False,
            "pattern": "^(true|TRUE)$",
        }
    }
}


@view_config(route_name='student_registration_statistics', request_method='POST')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def post_sr_extract_service(context, request):
    '''
    Handles POST request to /services/extract/student_registration_statistic

    :param context:  Pyramid context object
    :param request:  Pyramid request object
    '''

    params = convert_query_string_to_dict_arrays(request.json_body)

    return Response(body=json.dumps({'tasks': [{Extract.STATUS: Extract.OK}], 'filename': ""}), content_type='application/json')
