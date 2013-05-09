'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.security.roles.base import BaseRole


class TestBase(Unittest_with_smarter_sqlite):

    def test_append_context(self):
        base = BaseRole('connector')
        context = base.append_context("query", "guid")
        self.assertListEqual(context, [])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
