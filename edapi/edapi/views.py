'''
Created on Jan 14, 2013

@author: aoren
'''

from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed

from pyramid.view import view_config
from edapi import EDAPI_REPORTS_PLACEHOLDER
from edapi.utils import ReportNotFoundError, EdApiHTTPNotFound,\
    InvalidParameterError, EdApiHTTPPreconditionFailed, generate_report_config,\
    generate_report, report_config

def check_application_json(info, request):
    if 'application/json' == request.content_type.lower():
        return True

def get_report_registry(request, name = None):
    reg = request.registry.get(EDAPI_REPORTS_PLACEHOLDER)
    if (reg is None):
        raise ReportNotFoundError(name)
    return reg   

# returns list of reports in GET request    
@view_config(route_name='list_of_reports', renderer='json', request_method='GET')
def get_list_of_reports(request):
    try:
        reports = get_report_registry(request)
    except ReportNotFoundError:
        return []
    return list(reports.keys())

# handle the OPTIONS verb for the report resource
@view_config(route_name='report_get_option', renderer='json', request_method='OPTIONS')
def get_report_config(request):
    # gets the name of the report from the URL
    reportName = request.matchdict['name']
    # find the report configuration in the repository
    try:
        report_config = generate_report_config(get_report_registry(request, reportName), reportName)
    # if we cannot find the report configuration in the repository, we return 404 error
    except ReportNotFoundError as e:
        return EdApiHTTPNotFound(e.msg)
    except InvalidParameterError as e:
        return EdApiHTTPPreconditionFailed(e.msg)
    return report_config


@view_config(route_name='report_get_option', renderer='json', request_method='GET')
def generate_report_get(request):
    # gets the name of the report from the URL
    reportName = request.matchdict['name']
    
    params = request.GET
    
    try:
        report = generate_report(get_report_registry(request, reportName), reportName, params)
    except ReportNotFoundError as e:
        return EdApiHTTPNotFound(e.msg)
    except InvalidParameterError as e:
        return EdApiHTTPPreconditionFailed(e.msg)
    return report   

@view_config(route_name='report_post', renderer='json', request_method='POST', custom_predicates=(check_application_json,))
def generate_report_post(request):
    try:
        # basic check that it is a correct json, if not an exception will get raised when accessing json_body.
        report_config = request.json_body
        # gets the name of the report from the URL
        reportName = request.matchdict['name']
        report = generate_report(get_report_registry(request, reportName), reportName, report_config)
    except ReportNotFoundError as e:
        return EdApiHTTPNotFound(e.msg)
    except InvalidParameterError as e:
        return EdApiHTTPPreconditionFailed(e.msg)
    return report  
