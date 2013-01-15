'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.repository.report_config_repository import ReportConfigRepository
from pyramid.response import Response
from edapi.reports import ReportManager

def get_report_config(request):
    name = request.matchdict['name']
    repo = ReportConfigRepository()
    report_config = ReportManager.generate_report_config(name, repo)
    if (report_config is None):
        return Response('Not found!', status='404 Not Found')
    return report_config

def generate_report_get(request):
    reportName = request.matchdict['name']
    Request = request
    repo = ReportConfigRepository()
    return ReportManager.generate_report(reportName, Request.GET, repo)

def generate_report_post(request):
    if (request.content_type != 'application/json'):
        return Response('Not found!', status='404')
    Request = request 
    report_config = Request.json_body
    reportName = request.matchdict['name']
    repo = ReportConfigRepository()
    return ReportManager.generate_report(reportName, report_config, repo)
