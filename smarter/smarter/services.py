'''
Created on May 17, 2013

@author: dip
'''
from pyramid.view import view_config
from services.tasks.create_pdf import get_pdf_file
from urllib.parse import urljoin
from pyramid.response import Response
from smarter.security.context import select_with_context
from smarter.database.connector import SmarterDBConnection
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import and_
from edapi.exceptions import InvalidParameterError, ForbiddenError
from edauth.security.utils import get_session_cookie
import urllib.parse
import pyramid.threadlocal
from edapi.httpexceptions import EdApiHTTPPreconditionFailed,\
    EdApiHTTPForbiddenAccess, EdApiHTTPInternalServerError
from services.exceptions import PdfGenerationError


@view_config(route_name='pdf', request_method='POST', content_type='application/json')
def post_pdf_service(request):
    '''
    Handles POST request to /service/pdf
    '''
    try:
        params = request.json_body
    except ValueError:
        raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')

    return send_pdf_request(params)


@view_config(route_name='pdf', request_method='GET')
def get_pdf_service(request):
    '''
    Handles GET request to /service/pdf
    '''
    return send_pdf_request(request.GET)


def send_pdf_request(params):
    '''
    Requests for pdf content, throws http exceptions when error occurs
    '''
    try:
        response = get_pdf_content(params)
    except InvalidParameterError as e:
        raise EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        raise EdApiHTTPForbiddenAccess(e.msg)
    except PdfGenerationError as e:
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

    report = pyramid.threadlocal.get_current_request().matchdict['report'].lower()

    url = urljoin(pyramid.threadlocal.get_current_request().application_url, '/assets/html/' + report)

    # Encode the query parameters and append it to url
    encoded_params = urllib.parse.urlencode(params)
    url = url + "?%s" % encoded_params

    # check if pdf_stream is in file system
    file_name = '/tmp/test.pdf'

    # read pdf file
    (cookie_name, cookie_value) = get_session_cookie()
    pdf_stream = get_pdf_file(cookie_value, url, file_name, cookie_name=cookie_name)

    return Response(body=pdf_stream, content_type='application/pdf')


def has_context_for_pdf_request(student_guid):
    '''
    Validates that user has context to pdf (Individual student report)
    '''
    has_context = False
    with SmarterDBConnection() as connection:
        fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
        dim_student = connection.get_table(Constants.DIM_STUDENT)
        query = select_with_context([dim_student.c.student_guid],
                                    from_obj=[fact_asmt_outcome
                                              .join(dim_student, (fact_asmt_outcome.c.student_guid == dim_student.c.student_guid))])
        query = query.where(and_(fact_asmt_outcome.c.most_recent, fact_asmt_outcome.c.status == 'C', fact_asmt_outcome.c.student_guid == student_guid))
        results = connection.get_result(query)
    if results:
        has_context = True
    return has_context
