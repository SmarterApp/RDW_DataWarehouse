'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.repository.report_config_repository import ReportConfigRepository
import json
from distutils.tests.test_upload import Response

def get_report_config(request):
    name = request.matchdict['name']
    repo = ReportConfigRepository()
    json_obj = repo.get_report_config(name)
    if (json_obj is None):
        return Response('Not found!', status='404 Not Found')
    return json_obj

def generate_report_get(request):
    Request = request
    query = Request.GET["q"]
    params = json.dumps(query)
    repo = ReportConfigRepository()
    report = repo.get_report_config(params['alias'])

def generate_report_post(request):
    if (request.content_type != 'application/json'):
        return Response('Not found!', status='404')
    Request = request
    report_config = Request.json_body
    repo = ReportConfigRepository()
    reportName = request.matchdict['name']
    generate_report_method = repo.get_report_delegate(reportName)
    return generate_report_method(generate_report_method, report_config['params'])