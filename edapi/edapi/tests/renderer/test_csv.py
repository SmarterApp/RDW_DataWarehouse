# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Sep 27, 2013

@author: dip
'''
import unittest
from edapi.renderer.csv import CSVRenderer
from pyramid.response import Response
import platform


class DummyReq():
    response = Response()


class TestCSVRenderer(unittest.TestCase):

    def test_multi_rows(self):
        csv = CSVRenderer(None)
        value = {'header': ['a', 'b'], 'rows': [['1', '2'], ['c', 'd']], 'file_name': 'test.csv'}
        output = csv(value, {'request': DummyReq()})
        self.assertIsNotNone(output)
        # Check for non windows user
        if platform.system() != 'Windows':
            self.assertEqual('a,b\r\n1,2\r\nc,d\r\n', output)

    def test_with_one_row(self):
        csv = CSVRenderer(None)
        value = {'header': ['a', 'b'], 'rows': [['1', '2']], 'file_name': 'test.csv'}
        output = csv(value, {'request': DummyReq()})
        self.assertIsNotNone(output)
        if platform.system() != 'Windows':
            self.assertEqual('a,b\r\n1,2\r\n', output)

    def test_empty_results(self):
        csv = CSVRenderer(None)
        value = {'header': [], 'rows': [], 'file_name': 'test.csv'}
        output = csv(value, {'request': DummyReq()})
        self.assertIsNotNone(output)
        if platform.system() != 'Windows':
            self.assertEqual('\r\n', output)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
