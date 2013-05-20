'''
Created on May 17, 2013

@author: dip
'''
from pyramid.view import view_config
from services.tasks.create_pdf import generate_pdf, get_pdf_file, OK
from urllib.parse import urljoin, urlsplit, parse_qs
from pyramid.response import Response
from smarter.security.context import select_with_context
from smarter.database.connector import SmarterDBConnection
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import and_
from edapi.httpexceptions import EdApiHTTPPreconditionFailed,\
    EdApiHTTPForbiddenAccess, EdApiHTTPInternalServerError
from edapi.exceptions import InvalidParameterError, ForbiddenError
from smarter.exceptions import PdfGenerationError


@view_config(route_name='get_pdf')
def get_pdf(request):
    try:
        params = None
        
        # Get the query parameter or payload depending on verb 
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            try:
                params = request.json_body
            except ValueError:
                raise InvalidParameterError('Payload cannot be parsed')
        
        # the url received is partial url
        partial_url = params.get('url')
        if partial_url:
            url = urljoin(request.application_url, partial_url)
        else:
            raise InvalidParameterError('url is not found in query parameter')
            
        # Get query param
        split_url = urlsplit(url)
        query_params = parse_qs(split_url.query, keep_blank_values=True)
        student_guid = query_params.get('studentGuid')
        if student_guid:
            student_guid = student_guid[0]
        else:
            raise InvalidParameterError('studentGuid is not found in query parameter')
    
        if not has_context_for_pdf_request(student_guid):
            raise ForbiddenError('Access Denied')
        
        # check if pdf_stream is in file system
        # file_name = get_file_name_for_pdf(report_name, student_guid)
        file_name = '/tmp/' + student_guid + '.pdf'
        
        # read pdf file
        pdf_stream = get_pdf_file(file_name)
        if pdf_stream is None:
            # get registry to read settings
            cookie_name = request.registry.get('auth.policy.cookie_name', 'edware')
            
            # get the user cookie
            cookie = request.cookies[cookie_name]
            
            generate_task = generate_pdf(cookie, url, file_name, cookie_name=cookie_name)
            #result.wait
            if generate_task.result is OK:
                pdf_stream = get_pdf_file(file_name)
            else:
                raise PdfGenerationError()
    except InvalidParameterError as e:
        return EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        return EdApiHTTPForbiddenAccess(e.msg)
    except PdfGenerationError as e:
        return EdApiHTTPInternalServerError(e.msg)

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