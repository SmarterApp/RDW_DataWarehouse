'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.utils import generate_report_config, generate_report,\
    ReportNotFoundError, InvalidParameterError
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed
from pyramid.view import view_config

def check_application_json(info, request):
    if 'application/json' == request.content_type.lower():
        return True

# handle the OPTIONS verb for the report resource
@view_config(route_name='report', renderer='json', request_method='OPTIONS')
def get_report_config(request):
    # gets the name of the report from the URL
    name = request.matchdict['name']
    # find the report configuration in the repository
    try:
        report_config = generate_report_config(request.registry, name)
        # if we cannot find the report configuration in the repository, we return 404 error
    except ReportNotFoundError:
        return HTTPNotFound()
    except InvalidParameterError:
        return HTTPPreconditionFailed()
    return report_config


def convert_numbers_to_int(report_config):
    for (key, value) in report_config:
        if value.isdigit():
            report_config[key] = int(value)
    pass

@view_config(route_name='report', renderer='json', request_method='GET', custom_predicates=(check_application_json,))
def generate_report_get(request):
    # gets the name of the report from the URL
    reportName = request.matchdict['name'] 
    report_config = request.GET
    convert_numbers_to_int(report_config)
    
    try:
        report = generate_report(request.registry, reportName, report_config)
    except ReportNotFoundError:
        return HTTPNotFound()
    except InvalidParameterError:
        return HTTPPreconditionFailed()
    return report   

@view_config(route_name='report', renderer='json', request_method='POST', custom_predicates=(check_application_json,))
def generate_report_post(request):
    try:
        # basic check that it is a correct json, if not an exception will get raised when accessing json_body.
        report_config = request.json_body
        # gets the name of the report from the URL
        reportName = request.matchdict['name']
        report = generate_report(request.registry, reportName, report_config)
    except ReportNotFoundError:
        return HTTPNotFound()
    except InvalidParameterError:
        return HTTPPreconditionFailed()
    return report  
