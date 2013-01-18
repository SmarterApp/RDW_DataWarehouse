'''
Created on Jan 18, 2013

@author: dip
'''
import unittest
from edapi.utils import get_dict_value, generate_report, generate_report_config
from edapi.exceptions import ReportNotFoundError, InvalidParameterError
from edapi.tests.dummy import DummyValidator, Dummy

def dummy_method(params):
    return { "report" : params}

class TestUtils(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_get_dict_value_with_key_not_found(self):
        dictionary = {}
        key = "test"
        self.assertRaises(Exception, get_dict_value, dictionary, key)
    
    def test_get_dict_value_with_custom_exception(self):
        dictionary = {}
        key = "test"
        self.assertRaises(ReportNotFoundError, get_dict_value, dictionary, key, ReportNotFoundError)
  
    def test_get_dict_value_with_valid_key(self):      
        dictionary = {"test" : "value"}
        value = get_dict_value(dictionary, "test")
        self.assertEquals(value, dictionary.get("test"))
        
    def test_generate_report_with_failed_validation(self): 
        registry = {}
        report_name = "myTest"
        params = {"studentId" : 123}
        validator = DummyValidator(False)
        self.assertRaises(InvalidParameterError, generate_report, registry, report_name, params, validator)
    
    def test_generate_report_with_instantiate_obj(self):
        report_name = "myTest"
        config = {"id": {"type": "integer","required": True}}
        registry = {}
        registry[report_name] = { "params": config, "reference" : (Dummy,  Dummy.some_func)}
        params = {"id" : 123}
        validator = DummyValidator()
        response = generate_report(registry, report_name, params, validator)
        self.assertEqual(response, {"report" : params})
    
    def test_generate_report_with_obj_as_func(self):
        report_name = "myTest"
        config = {"id": {"type": "integer","required": True}}
        registry = {}
        registry[report_name] = { "params": config, "reference" : (dummy_method,  dummy_method)}
        params = {"id" : 123}
        validator = DummyValidator()
        response = generate_report(registry, report_name, params, validator)
        self.assertEqual(response, {"report" : params})
    
    def test_generate_report_config_with_invalid_report_name(self):
        registry = {}
        registry["myTest"] = {}
        self.assertRaises(ReportNotFoundError, generate_report_config, registry, "reportDoesNotExist")
    
    def test_generate_report_config_with_missing_param(self):
        report_name = "myTest"
        registry = {}
        registry[report_name] = {}
        self.assertRaises(InvalidParameterError, generate_report_config, registry, report_name)
    
    def test_generate_report_config_with_valid_param(self):
        report_name = "myTest"
        config = {"id": {"type": "integer","required": True}}
        registry = {}
        registry[report_name] = { "params": config, "reference" : (dummy_method,  dummy_method)}
        response = generate_report_config(registry, report_name)
        self.assertEquals(response, config)
     

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()