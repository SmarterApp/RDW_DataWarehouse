'''
Created on Sep 27, 2013

@author: dip
'''
import unittest
from edapi.renderer.csv import CSVRenderer
from pyramid.response import Response


class DummyReq():
    response = Response()


class TestCSVRenderer(unittest.TestCase):

    def test_multi_rows(self):
        csv = CSVRenderer(None)
        value = {'header': ['a', 'b'], 'rows': [['1', '2'], ['c', 'd']], 'file_name': 'test.csv'}
        output = csv(value, {'request': DummyReq()})
        self.assertIsNotNone(output)
        self.assertEqual('a,b\r\n1,2\r\nc,d\r\n', output)

    def test_with_one_row(self):
        csv = CSVRenderer(None)
        value = {'header': ['a', 'b'], 'rows': [['1', '2']], 'file_name': 'test.csv'}
        output = csv(value, {'request': DummyReq()})
        self.assertIsNotNone(output)
        self.assertEqual('a,b\r\n1,2\r\n', output)

    def test_empty_results(self):
        csv = CSVRenderer(None)
        value = {'header': [], 'rows': [], 'file_name': 'test.csv'}
        output = csv(value, {'request': DummyReq()})
        self.assertIsNotNone(output)
        self.assertEqual('\r\n', output)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
