'''
Created on May 17, 2013

@author: dip
'''
from pyramid.view import view_config
from services.tasks.create_pdf import generate_pdf, get_pdf_file, OK
from urllib.parse import urljoin
from pyramid.response import Response
from smarter.security.context import select_with_context
from smarter.database.connector import SmarterDBConnection
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import and_
from edapi.exceptions import InvalidParameterError, ForbiddenError
from smarter.exceptions import PdfGenerationError
from edauth.security.utils import get_session_cookie
import urllib.parse
import pyramid.threadlocal


@view_config(route_name='pdf', request_method='POST')
def post_pdf_serivce_post(request):
    '''
    Handles POST request to /service/pdf
    '''
    try:
        params = request.json_body
    except ValueError:
        raise InvalidParameterError('Payload cannot be parsed')

    return get_pdf_content(params)


@view_config(route_name='pdf', request_method='GET')
def get_pdf_serivce(request):
    '''
    Handles GET request to /service/pdf
    '''
    return get_pdf_content(request.GET)


def get_pdf_content(params):
    student_guid = params.get('studentGuid')

    if not has_context_for_pdf_request(student_guid):
        raise ForbiddenError('Access Denied')

    report = pyramid.threadlocal.get_current_request().matchdict['report'].lower()

    if report == 'individual_student_report':
        url = urljoin(pyramid.threadlocal.get_current_request().application_url, '/assets/html/indivStudentReport.html')

    encoded_params = urllib.parse.urlencode(params)
    url = url + "?%s" % encoded_params

    # check if pdf_stream is in file system
    # file_name = get_file_name_for_pdf(report_name, student_guid)
    file_name = '/tmp/' + student_guid + '.pdf'

    # read pdf file
    pdf_stream = get_pdf_file(file_name)
    if pdf_stream is None:
        (cookie_name, cookie_value) = get_session_cookie()

        generate_task = generate_pdf(cookie_value, url, file_name, cookie_name=cookie_name)
        if generate_task is OK:
            pdf_stream = get_pdf_file(file_name)
        else:
            raise PdfGenerationError()

    return Response(body=pdf_stream, content_type='application/pdf')


def has_context_for_pdf_request(student_guid):
    has_context = False
    with SmarterDBConnection() as connection:
        # TODO, do I need section_guid here?
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
