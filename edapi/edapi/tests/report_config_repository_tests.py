'''
Created on Jan 16, 2013

@author: dip
'''
import unittest
from edapi.repository.report_config_repository import ReportConfigRepository

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        repo = ReportConfigRepository()
        params = {"alias":"test", "other":"value"}
        repo.add(None, **params)
        assert(repo.get_report_count() == 1)
        params['alias'] = "test2"
        repo.add(None, **params)
        assert(repo.get_report_count() == 2)
        
    def test_get_report_config(self):
        repo = ReportConfigRepository()
        config = repo.get_report_config("reportDoesNotExist")
        assert(config is None)
        
        params = {"alias":"test", "params": "{\"student_id\":{}, \"assessment_id\":{}}"}
        repo.add(None, **params)
        config = repo.get_report_config(params['alias'])
        assert(config is params['params'])
        
        params = {"alias":"test2"}
        repo.add(None, **params)
        config = repo.get_report_config(params['alias'])
        assert(config is None)
    
    def test_get_report_delegate(self):
        repo = ReportConfigRepository()
        params = {"alias":"test", "params": "{\"student_id\":{}, \"assessment_id\":{}}"}
        repo.add(repo, **params)
        delegate = repo.get_report_delegate(params['alias'])
        assert(repo is delegate)
        
        delegate = repo.get_report_delegate("reportDoesNotExist")
        assert(delegate is None)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()