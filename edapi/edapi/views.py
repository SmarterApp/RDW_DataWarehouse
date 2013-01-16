'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.utils import generate_report_config, generate_report
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed

def get_report_config(request):
    name = request.matchdict['name']
    report_config = generate_report_config(name)
    if (report_config is None):
        return HTTPNotFound()
    return report_config

def generate_report_get(request):
    Request = request
    reportName = request.matchdict['name'] 
    report_config = Request.GET
    return generate_report(reportName, report_config)

def generate_report_post(request):
    if (request.content_type != 'application/json'):
        return HTTPNotFound()
    Request = request 
    
    try:
        # basic check that it is a correct json, if not an exception will get raised when accessing json_body.
        report_config = Request.json_body
        #break
    except:
        return HTTPPreconditionFailed()
    
    reportName = request.matchdict['name']
    return generate_report(reportName, report_config)
