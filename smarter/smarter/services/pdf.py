'''
Created on May 17, 2013

@author: dip
'''
from pyramid.view import view_config
from services.tasks.pdf import get
from urllib.parse import urljoin
from pyramid.response import Response
from smarter.security.context import check_context
from edapi.exceptions import InvalidParameterError, ForbiddenError
from edauth.security.utils import get_session_cookie
import urllib.parse
import pyramid.threadlocal
from edapi.httpexceptions import EdApiHTTPPreconditionFailed, \
    EdApiHTTPForbiddenAccess, EdApiHTTPInternalServerError, EdApiHTTPNotFound
from services.exceptions import PdfGenerationError
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from smarter.reports.helpers.constants import AssessmentType, Constants
import services.celery
from edapi.decorators import validate_params
from edcore.utils.utils import to_bool


KNOWN_REPORTS = ['indivstudentreport.html']

PDF_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        Constants.STATECODE: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z]{2}$"},
        Constants.STUDENTGUID: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"},
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
        }
    }
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
    except:
        # if celery get task got timed out...
        raise EdApiHTTPInternalServerError("Internal Error")

    return response


def get_pdf_content(params):
    '''
    Read pdf content from file system if it exists, else generate it

    :param params: python dict that contains query parameters from the request
    '''
    student_guid = params.get(Constants.STUDENTGUID)
    state_code = params.get(Constants.STATECODE)
    asmt_type = params.get(Constants.ASMTTYPE, AssessmentType.SUMMATIVE)
    effective_date = str(params.get(Constants.EFFECTIVEDATE))
    if student_guid is None:
        raise InvalidParameterError('Required parameter is missing')

    if not has_context_for_pdf_request(state_code, student_guid):
        raise ForbiddenError('Access Denied')

    asmt_type = asmt_type.upper()
    if asmt_type not in [AssessmentType.SUMMATIVE, AssessmentType.INTERIM_COMPREHENSIVE]:
        raise InvalidParameterError('Unknown assessment type')

    report = pyramid.threadlocal.get_current_request().matchdict['report']

    url = urljoin(pyramid.threadlocal.get_current_request().application_url, '/assets/html/' + report)

    # Encode the query parameters and append it to url
    encoded_params = urllib.parse.urlencode(params)
    url = url + "?%s" % encoded_params

    # check for gray scale request
    is_grayscale = bool(params.get('grayscale', 'false').lower() == 'true')
    # read language
    lang = params.get('lang', 'en').lower()

    # get isr file path name
    pdf_base_dir = pyramid.threadlocal.get_current_registry().settings.get('pdf.report_base_dir', "/tmp")
    file_name = generate_isr_report_path_by_student_guid(state_code, effective_date, pdf_report_base_dir=pdf_base_dir, student_guid=student_guid, asmt_type=asmt_type, grayScale=is_grayscale, lang=lang)

    # get current session cookie and request for pdf
    (cookie_name, cookie_value) = get_session_cookie()
    celery_timeout = int(pyramid.threadlocal.get_current_registry().settings.get('pdf.celery_timeout', '30'))
    always_generate = to_bool(pyramid.threadlocal.get_current_registry().settings.get('pdf.always_generate', False))
    celery_response = get.delay(cookie_value, url, file_name, cookie_name=cookie_name, timeout=services.celery.TIMEOUT, grayscale=is_grayscale, always_generate=always_generate)  # @UndefinedVariable
    pdf_stream = celery_response.get(timeout=celery_timeout)

    return Response(body=pdf_stream, content_type='application/pdf')


def has_context_for_pdf_request(state_code, student_guid):
    '''
    Validates that user has context to student_guid

    :param student_guid:  guid of the student
    '''
    if type(student_guid) is not list:
        student_guid = [student_guid]
    return check_context(state_code, student_guid)
