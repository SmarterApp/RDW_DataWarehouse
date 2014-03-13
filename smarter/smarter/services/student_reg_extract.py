from pyramid.response import Response
from pyramid.view import view_config
from edapi.decorators import validate_params
from edapi.logging import audit_event
from edapi.utils import convert_query_string_to_dict_arrays
from smarter.reports.helpers.constants import Constants

STUDENT_REGISTRATION_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        Constants.ACADEMIC_YEAR: {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^\d{4}$"
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": True
        }
    }
}


@view_config(route_name='student_registration_statistics', request_method='GET')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def get_sr_extract_service(context, request):
    '''
    Handles GET request to /services/extract/student_registration_statistic

    :param request:  Pyramid request object
    '''

    params = convert_query_string_to_dict_arrays(request.GET)

    return Response()


@view_config(route_name='student_registration_statistics', request_method='POST')
@validate_params(schema=STUDENT_REGISTRATION_PARAMS)
@audit_event()
def post_sr_extract_service(context, request):
    '''
    Handles GET request to /services/extract/student_registration_statistic

    :param request:  Pyramid request object
    '''

    params = convert_query_string_to_dict_arrays(request.GET)

    return Response()
