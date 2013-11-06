'''
Created on Nov 5, 2013

@author: ejen
'''
import unittest
from edextract.celery import setup_global_settings, setup_celery, celery
from edextract.tasks.query import handle_request, is_available, generate_csv


class TestQuery(unittest.TestCase):

    def test_handle_request(self):
        pass

    def test_is_available(self):
        pass

    def test_generate_csv(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()