'''
Created on Jan 17, 2013

@author: dip
'''
import unittest
from edapi.views import (                        
get_report_registry, 
get_list_of_reports,
get_report_config,
generate_report_get,
generate_report_post,
check_content_type, 
get_request_body)
from edapi import EDAPI_REPORTS_PLACEHOLDER, add_report_config
from edapi.tests.dummy import Dummy, DummyRequest, DummyValidator
from edapi.exceptions import ReportNotFoundError, InvalidParameterError
from edapi.httpexceptions import EdApiHTTPNotFound, EdApiHTTPPreconditionFailed,\
    EdApiHTTPRequestURITooLong
import json

class TestViews(unittest.TestCase):
    
    # setting up the test class
    def setUp(self):
        self.request = DummyRequest()
        self.request.reset()
        
    # tearing down the test class
    def tearDown(self):
        self.request = None
        
    def test_check_application_json(self):
        check_application_json = check_content_type("application/json") 
        self.request.content_type = "dummy"
        val = check_application_json(None, self.request)
        self.assertFalse(val)
        
        self.request.content_type = "APPLIcation/jsOn"
        val = check_application_json(None, self.request)
        self.assertTrue(val)
    
    def test_get_report_registry_with_no_placehold_undefined(self):
        self.assertRaises(ReportNotFoundError, get_report_registry, self.request)
    
    def test_get_list_of_reports_with_placeholder_undefined(self):
        resp = get_list_of_reports(self.request)
        self.assertEqual(resp, [])
        
    def test_get_list_of_reports_with_zero_reports(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        reports = get_list_of_reports(self.request)
        self.assertEqual(reports, [])
    
    def test_get_list_of_reports_with_nonempty_reports(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {}
        reports = get_list_of_reports(self.request)
        self.assertEqual(reports, ["test"])
        
    def test_get_report_confg_for_report_not_in_registry(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
      
        self.request.matchdict['name'] = "testNotFound"    
        response = get_report_config(self.request)
        self.assertIs(type(response), EdApiHTTPNotFound)
    
    def test_get_report_confg_for_report_in_registry_with_no_params(self):  
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}      
        self.request.matchdict['name'] = "test"
        response = get_report_config(self.request)
        self.assertEqual(response.json, {})
        
        
    def test_get_report_confg_for_valid_request(self):  
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}      
        self.request.matchdict['name'] = "test"
        params = {"studentId": {"validation" : {"type":"integer", "required":True}}}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params}
        response = get_report_config(self.request)
        self.assertEqual(response.json, params)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.allow, ("GET","POST","OPTIONS"))
        
    def test_generate_report_get_for_report_not_in_registry(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
      
        self.request.matchdict['name'] = "testNotFound"    
        response = generate_report_get(self.request)
        self.assertIs(type(response),  EdApiHTTPNotFound)
    
    def test_generate_report_get_for_report_with_no_params(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
        
        self.request.matchdict['name'] = "test"
        response = generate_report_get(self.request)
        self.assertIs(type(response), EdApiHTTPPreconditionFailed)
        
    def test_generate_report_get_for_valid_request(self):
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.matchdict['name'] = "test"

        validator = DummyValidator()
        params = {"studentId": {"type": "integer","required": True}}
        self.request.GET = {"studentId" : 123}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params, "reference" : (Dummy,  Dummy.some_func)}
        response = generate_report_get(self.request, validator)
        self.assertEqual(response, {"report": self.request.GET})
        
    def test_generate_report_post_for_report_not_in_registry(self):
        self.request.content_type = "application/json"
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
        self.request.json_body = "{'a':1}"
        
        self.request.matchdict['name'] = "testNotFound"    
        response = generate_report_post(self.request)
        self.assertIs(type(response), EdApiHTTPNotFound)
    
    def test_generate_report_post_for_report_with_no_param(self):
        self.request.content_type = "application/json"
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
        self.request.json_body = "{'a':1}"
   
        self.request.matchdict['name'] = "test"
        response = generate_report_post(self.request)
        self.assertIs(type(response), EdApiHTTPPreconditionFailed)
    
    def test_generate_report_post_for_valid_request(self):
        self.request.content_type = "application/json"
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"some":"thing"}
        self.request.matchdict['name'] = "test"

        params = {"studentId": {"type": "string","required": True}}
        self.request.json_body = {"studentId" : "123"}
        validator = DummyValidator()
        self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"] = {"params":params, "reference" : (Dummy,  Dummy.some_func)}
        response = generate_report_post(self.request, validator)
        self.assertEqual(response, {"report": self.request.json_body})
    
    # tests for add_report_config from __init__.py  
    def test_add_report_config_with_no_reports_placeholder(self):
        dummy = Dummy()
        add_report_config(self.request, dummy)
        self.assertEquals(self.request.registry[EDAPI_REPORTS_PLACEHOLDER],{})
    
    def test_add_report_config_with_reports_placeholder(self):
        dummy = Dummy()
        add_report_config(self.request, dummy, name = "test", params = {})
        self.assertEqual(self.request.registry[EDAPI_REPORTS_PLACEHOLDER]["test"], {"name":"test", "params": {}, "reference" : dummy})
        
    def test_get_request_body(self):
        request = DummyValueError()
        self.assertRaises(InvalidParameterError, get_request_body, request)
        
    def test_url_too_long_in_get_request(self):
        self.request.url = 'h' * 2001
        response = generate_report_get(self.request)
        self.assertIs(type(response), EdApiHTTPRequestURITooLong)

class DummyValueError:
    '''
    A dummy class that can has a method that triggers ValueError exception
    '''
    @property
    def json_body(self):
        return json.loads('error')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_report_registry']
    unittest.main()