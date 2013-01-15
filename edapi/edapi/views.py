'''
Created on Jan 14, 2013

@author: aoren
'''
from pyramid.view import view_config
from edapi.repository.report_config_repository import ReportConfigRepository
import json
from distutils.tests.test_upload import Response

def get_report_config(request):
    name = request.matchdict['name']
    repo = ReportConfigRepository()
    json_obj = repo.get_report_config(name)
    return json_obj

def generate_report_get(request):
    Request = request
    query = Request.GET["_query"]
    params = json.dumps(query)
    repo = ReportConfigRepository()
    report = repo.get_report_config(params['alias'])

def generate_report_post(request):
    if (request.content_type != 'application/json'):
        return Response('Not found!', status='404 Not Found')
    Request = request
    body = Request.json_body
    report_config = Request.json_body
    repo = ReportConfigRepository()
    reportName = report_config['alias']
    report = repo.get_report(reportName)
    data = report(report, report_config['params'])
    return data