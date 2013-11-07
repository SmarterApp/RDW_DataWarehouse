'''
Created on Nov 5, 2013

@author: ejen
'''
import unittest
from edextract.celery import setup_global_settings, setup_celery, celery
from edextract.tasks.smart_query import process_extraction_request


class TestSmarterQuery(unittest.TestCase):

    def test_process_extraction_request(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
