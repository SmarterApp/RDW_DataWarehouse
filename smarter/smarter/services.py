'''
Created on May 17, 2013

@author: dip
'''
from pyramid.view import view_config
from services.tasks.create_pdf import get_pdf
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
from smarter.reports.helpers.constants import Constants
import services.celeryconfig


KNOWN_REPORTS = ['indivstudentreport.html']


@view_config(route_name='pdf', request_method='POST', content_type='application/json')
def post_pdf_service(request):
    '''
    Handles POST request to /services/pdf
    '''
    try:
        params = request.json_body
    except ValueError:
        raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')

    return send_pdf_request(params)


@view_config(route_name='pdf', request_method='GET')
def get_pdf_service(request):
    '''
    Handles GET request to /services/pdf
    '''
    return send_pdf_request(request.GET)


def send_pdf_request(params):
    '''
    Requests for pdf content, throws http exceptions when error occurs
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
    except PdfGenerationError as e:
        raise EdApiHTTPInternalServerError(e.msg)
    except TimeoutError as e:
        # if celery get task got timed out...
        raise EdApiHTTPInternalServerError(e.msg)

    return response


def get_pdf_content(params):
    '''
    Read pdf content from file system if it exists, else generate it
    '''
    student_guid = params.get('studentGuid')
    if student_guid is None:
        raise InvalidParameterError('Required parameter is missing')

    if not has_context_for_pdf_request(student_guid):
        raise ForbiddenError('Access Denied')

    report = pyramid.threadlocal.get_current_request().matchdict['report']

    url = urljoin(pyramid.threadlocal.get_current_request().application_url, '/assets/html/' + report)

    # Encode the query parameters and append it to url
    encoded_params = urllib.parse.urlencode(params)
    url = url + "?%s" % encoded_params

    # check for gray scale request
    is_grayscale = bool(params.get('grayscale', 'false').lower() == 'true')

    # get isr file path name
    pdf_base_dir = pyramid.threadlocal.get_current_registry().settings.get('pdf.report_base_dir', "/tmp")
    file_name = generate_isr_report_path_by_student_guid(pdf_report_base_dir=pdf_base_dir, student_guid=student_guid, asmt_type=Constants.SUMMATIVE, grayScale=is_grayscale)

    # get current session cookie and request for pdf
    (cookie_name, cookie_value) = get_session_cookie()
    celery_timeout = int(pyramid.threadlocal.get_current_registry().settings.get('pdf.celery_timeout', '30'))
    mkdir_mode = int(pyramid.threadlocal.get_current_registry().settings.get('pdf.mkdir_mode', '0700'))
    celery_response = get_pdf.delay(cookie_value, url, file_name, cookie_name=cookie_name, timeout=services.celeryconfig.TIMEOUT, grayScale=is_grayscale, mkdir_mode=mkdir_mode)  # @UndefinedVariable
    pdf_stream = celery_response.get(timeout=celery_timeout)

    return Response(body=pdf_stream, content_type='application/pdf')


def has_context_for_pdf_request(student_guid):
    '''
    Validates that user has context to student_guid
    '''
    if type(student_guid) is not list:
        student_guid = [student_guid]
    return check_context(student_guid)
