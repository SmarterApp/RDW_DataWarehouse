'''
Created on Jan 14, 2013

@author: aoren
'''
from pyramid.view import view_config
from edapi.repository.report_config_repository import ReportConfigRepository
import json
from distutils.tests.test_upload import Response

@view_config(route_name='report', renderer='json', request_method='OPTIONS')
def get_report_config(request):
    name = request.matchdict['name']
    repo = ReportConfigRepository()
    json_obj = repo.get_report_config(name)
    return json_obj

@view_config(route_name='report', renderer='json', request_method='GET')
def generate_report_get(request):
    Request = request
    query = Request.GET["_query"]
    params = json.dumps(query)
    repo = ReportConfigRepository()
    report = repo.get_report_config(params['alias'])

@view_config(route_name='report', renderer='json', request_method='POST')
def generate_report_post(request):
    if (request.content_type != 'application/json'):
        return Response('Not found, dude!', status='404 Not Found')
    Request = request
    body = Request.json_body
    report_config = Request.json_body
    repo = ReportConfigRepository()
    reportName = report_config['alias']
    report = repo.get_report(reportName)
    data = report(report, report_config['params'])
    return data