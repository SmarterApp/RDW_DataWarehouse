'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.security.roles.base import BaseRole


class TestBase(unittest.TestCase):

    def test_append_context(self):
        base = BaseRole('connector')
        context = base.get_context("guid")
        self.assertIsNone(context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
