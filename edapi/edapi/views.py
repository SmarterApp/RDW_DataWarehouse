'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.repository.report_config_repository import IReportConfigRepository
from pyramid.response import Response
from zope import component
from edapi.utils import generate_report_config, generate_report

def get_report_config(request):
    name = request.matchdict['name']
    report_config = generate_report_config(name)
    if (report_config is None):
        return Response('Not found!', status='404 Not Found')
    return report_config

def generate_report_get(request):
    Request = request
    reportName = request.matchdict['name']
    report_config = Request.GET
    return generate_report(reportName, report_config)

def generate_report_post(request):
    if (request.content_type != 'application/json'):
        return Response('Not found!', status='404')
    Request = request 
    
    try:
        # basic check that it is a correct json, if not an exception will get raised when accessing json_body.
        report_config = Request.json_body
        #break
    except:
        return Response('invalid parameters', status='412')
    
    reportName = request.matchdict['name']
    repo = component.getUtility(IReportConfigRepository)
    return generate_report(reportName, report_config, repo)
