'''
Created on Jan 17, 2013

@author: dip
'''
import unittest
from edapi.views import (
check_application_json,                         
get_report_registry, 
get_list_of_reports,
get_report_config,
generate_report_get,
generate_report_post)
from edapi.utils import ReportNotFoundError, EdApiHTTPNotFound,\
    EdApiHTTPPreconditionFailed
from edapi import EDAPI_REPORTS_PLACEHOLDER

class DummyRequest:
    registry = {}
    matchdict = {}
    content_type = ''
    GET = {}
    json_body = {}

class TestViews(unittest.TestCase):
    
    # setting up the test class
    def setUp(self):
        self.request = DummyRequest()
        self.request.registry = {}
        self.request.matchdict = {}
        self.request.content_type = ''
        self.request.GET = {}
        self.request.json_body = {}

    # tearing down the test class
    def tearDown(self):
        self.request = None
        
    def test_check_application_json(self):
        self.request.content_type = "dummy"
        val = check_application_json(None, self.request)
        assert(val is None)
        
        self.request.content_type = "APPLIcation/jsOn"
        val = check_application_json(None, self.request)
        assert(val is True)
    
    def test_get_report_registry(self):
        testPass = False
        try:
            get_report_registry(self.request)
        except ReportNotFoundError:
            testPass = True
        assert(testPass)
        
    def test_get_list_of_reports(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        reports = get_list_of_reports(self.request)
        assert(reports == [])
        
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {}
        reports = get_list_of_reports(self.request)
        assert(reports == ["test"])
        
    def test_get_report_config(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
      
        self.request.matchdict['name'] = "testNotFound"    
        response = get_report_config(self.request)
        assert(type(response) is EdApiHTTPNotFound)
        
        self.request.matchdict['name'] = "test"
        response = get_report_config(self.request)
        assert(type(response) is EdApiHTTPPreconditionFailed)

        params = {"studentId": {"validation" : {"type":"integer", "required":True}}}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params}
        response = get_report_config(self.request)
        assert(response == params)
        
    def test_generate_report_get(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
      
        self.request.matchdict['name'] = "testNotFound"    
        response = generate_report_get(self.request)
        assert(type(response) is EdApiHTTPNotFound)
        
        self.request.matchdict['name'] = "test"
        response = generate_report_get(self.request)
        assert(type(response) is EdApiHTTPPreconditionFailed)

        params = {"studentId": {"validation" : {"type":"integer", "required":False}}}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params}
        response = generate_report_get(self.request)
        #TODO get a valid response
        
    def test_generate_report_post(self):
        self.request.content_type = "application/json"
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
        self.request.json_body = "{'a':1}"
        
        self.request.matchdict['name'] = "testNotFound"    
        response = generate_report_post(self.request)
        assert(type(response) is EdApiHTTPNotFound)
        
        self.request.matchdict['name'] = "test"
        response = generate_report_post(self.request)
        assert(type(response) is EdApiHTTPPreconditionFailed)

        params = {"studentId": {"validation" : {"type":"integer", "required":False}}}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params}
        #response = generate_report_post(self.request)
        #TODO get a valid response
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_report_registry']
    unittest.main()