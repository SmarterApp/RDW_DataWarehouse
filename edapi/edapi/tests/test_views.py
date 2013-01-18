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
from edapi.tests.dummy import Dummy, DummyRequest, DummyValidator

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
        self.assertIsNone(val)
        
        self.request.content_type = "APPLIcation/jsOn"
        val = check_application_json(None, self.request)
        self.assertTrue(val)
    
    def test_get_report_registry(self):
        testPass = False
        try:
            get_report_registry(self.request)
        except ReportNotFoundError:
            testPass = True
        self.assertTrue(testPass)
        
    def test_get_list_of_reports(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        reports = get_list_of_reports(self.request)
        self.assertEqual(reports, [])
        
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {}
        reports = get_list_of_reports(self.request)
        self.assertEqual(reports, ["test"])
        
    def test_get_report_config(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
      
        self.request.matchdict['name'] = "testNotFound"    
        response = get_report_config(self.request)
        self.assertIs(type(response), EdApiHTTPNotFound)
        
        self.request.matchdict['name'] = "test"
        response = get_report_config(self.request)
        self.assertIs(type(response), EdApiHTTPPreconditionFailed)

        params = {"studentId": {"validation" : {"type":"integer", "required":True}}}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params}
        response = get_report_config(self.request)
        self.assertEqual(response, params)
        
    def test_generate_report_get(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
      
        self.request.matchdict['name'] = "testNotFound"    
        response = generate_report_get(self.request)
        self.assertIs(type(response),  EdApiHTTPNotFound)
        
        self.request.matchdict['name'] = "test"
        response = generate_report_get(self.request)
        self.assertIs(type(response), EdApiHTTPPreconditionFailed)

        validator = DummyValidator()
        params = {"studentId": {"type": "integer","required": True}}
        self.request.GET = {"studentId" : 123}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params, "reference" : (Dummy,  Dummy.some_func)}
        response = generate_report_get(self.request, validator)
        self.assertEqual(response, {"report": self.request.GET})
        
    def test_generate_report_post(self):
        self.request.content_type = "application/json"
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
        self.request.json_body = "{'a':1}"
        
        self.request.matchdict['name'] = "testNotFound"    
        response = generate_report_post(self.request)
        self.assertIs(type(response), EdApiHTTPNotFound)
        
        self.request.matchdict['name'] = "test"
        response = generate_report_post(self.request)
        self.assertIs(type(response), EdApiHTTPPreconditionFailed)

        params = {"studentId": {"type": "string","required": True}}
        self.request.json_body = {"studentId" : "123"}
        validator = DummyValidator()
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params, "reference" : (Dummy,  Dummy.some_func)}
        response = generate_report_post(self.request, validator)
        self.assertEqual(response, {"report": self.request.json_body})
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_report_registry']
    unittest.main()