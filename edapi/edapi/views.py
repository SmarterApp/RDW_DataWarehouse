'''
Handles requests to endpoints

Created on Jan 14, 2013

@author: aoren
'''
from pyramid.view import view_config
from edapi.utils import generate_report_config,\
    generate_report, EDAPI_REPORTS_PLACEHOLDER
from edapi.exceptions import ReportNotFoundError, InvalidParameterError,\
    ForbiddenError
from edapi.httpexceptions import EdApiHTTPNotFound, EdApiHTTPPreconditionFailed,\
    EdApiHTTPRequestURITooLong, EdApiHTTPForbiddenAccess
from pyramid.response import Response
import json

MAX_REQUEST_URL_LENGTH = 2000


def get_report_registry(request, name=None):
    '''
    given a request, return the registry belonging to edapi reports
    @param name: the report name that is trying to get the registry (will get used if the registry is not found)
    @type name: string
    '''
    reg = request.registry.get(EDAPI_REPORTS_PLACEHOLDER)
    if (reg is None):
        raise ReportNotFoundError(name)
    return reg


def get_request_body(request):
    '''
    returns pyramid request body as json, throws exception if request.json_body isn't valid json

    @param request: the request object
    @type request: request
    '''
    try:
        body = request.json_body
    except ValueError:
        raise InvalidParameterError
    return body


@view_config(route_name='list_of_reports', renderer='json', request_method='GET')
def get_list_of_reports(request):
    '''
    returns list of reports in GET request
    '''
    try:
        reports = get_report_registry(request)
    except ReportNotFoundError:
        return []
    return list(reports.keys())


@view_config(route_name='report_get_option_post', renderer='json', request_method='OPTIONS')
def get_report_config(request):
    '''
    handle the OPTIONS verb for data resource

    @param request: the request object
    @type request: request
    '''
    # gets the name of the report from the URL
    reportName = request.matchdict['name']
    # find the report configuration in the repository
    try:
        report_config = generate_report_config(get_report_registry(request, reportName), reportName)
    # if we cannot find the report configuration in the repository, we return 404 error
    except ReportNotFoundError as e:
        return EdApiHTTPNotFound(e.msg)
    return Response(body=json.dumps(report_config), content_type="application/json", allow='GET,POST,OPTIONS')


@view_config(route_name='report_get_option_post', renderer='json', request_method='GET', content_type="application/json",)
def generate_report_get(request, validator=None):
    '''
    handle GET verb for data resource

    @param request: the request object
    @type request: request
    @param validator: the request object
    @type request: request
    '''

    # if full request URL with query string is too long
    if (len(request.url) > MAX_REQUEST_URL_LENGTH):
        return EdApiHTTPRequestURITooLong(MAX_REQUEST_URL_LENGTH)

    # gets the name of the report from the URL
    reportName = request.matchdict['name']

    params = request.GET

    try:
        report = generate_report(get_report_registry(request, reportName), reportName, params, validator)
    except ReportNotFoundError as e:
        return EdApiHTTPNotFound(e.msg)
    except InvalidParameterError as e:
        return EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        return EdApiHTTPForbiddenAccess(e.msg)
    return report


@view_config(route_name='report_get_option_post', renderer='json', request_method='POST', content_type="application/json",)
def generate_report_post(request, validator=None):
    '''
    handle POST verb for data resource

    @param request: the request object
    @type request: request
    @param validator: the request object
    @type request: request
    '''
    try:
        # basic check that it is a correct json, if not an exception will get raised when accessing json_body.
        report_config = get_request_body(request)
        # gets the name of the report from the URL
        reportName = request.matchdict['name']
        report = generate_report(get_report_registry(request, reportName), reportName, report_config, validator)
    except ReportNotFoundError as e:
        return EdApiHTTPNotFound(e.msg)
    except InvalidParameterError as e:
        return EdApiHTTPPreconditionFailed(e.msg)
    except ForbiddenError as e:
        return EdApiHTTPForbiddenAccess(e.msg)
    return report
