'''
Created on Jan 14, 2013

@author: aoren
'''
from pyramid.view import view_config
from edapi.repository.report_config_repository import ReportConfigRepository
import json

@view_config(route_name='report', renderer='json', request_method='OPTIONS')
def get_selection(request):
    name = request.matchdict['name']
    repo = ReportConfigRepository()
    json_obj = repo.get_config( name + ".json")
    return {'result' : json_obj}

@view_config(route_name='report', renderer='json', request_method='GET')
def generate_report_get(request):
    Request = request
    query = Request.params()["q"]
    print(query)
    report_config = json.dumps(query)
    print (report_config)
    

@view_config(route_name='report', renderer='json', request_method='POST')
def generate_report_post(request):
    Request = request
    body = Request.json_body
    print(body)
    report_config = json.dumps(body)
    print (report_config)