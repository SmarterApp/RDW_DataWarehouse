'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.utils import generate_report_config, generate_report
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed
from pyramid.view import view_config

# handle the OPTIONS verb for the report resource
@view_config(route_name='report', renderer='json', request_method='OPTIONS')
def get_report_config(request):
    # gets the name of the report from the URL
    name = request.matchdict['name']
    # find the report configuration in the repository
    report_config = generate_report_config(request.registry, name)
    # if we cannot find the report configuration in the repository, we return 404 error
    if (report_config is None):
        return HTTPNotFound()
    return report_config

@view_config(route_name='report', renderer='json', request_method='GET')
def generate_report_get(request):
    # gets the name of the report from the URL
    reportName = request.matchdict['name'] 
    report_config = request.GET
    return generate_report(request.registry, reportName, report_config)

@view_config(route_name='report_for_post', renderer='json', request_method='POST')
def generate_report_post(request):
    # if the media type is not application/json, the request is rejected.
    if (request.content_type != 'application/json'):
        return HTTPNotFound()
    
    try:
        # basic check that it is a correct json, if not an exception will get raised when accessing json_body.
        report_config = request.json_body
        #break
    except:
        return HTTPPreconditionFailed()
    # gets the name of the report from the URL
    reportName = request.matchdict['name']
    return generate_report(request.registry, reportName, report_config)
