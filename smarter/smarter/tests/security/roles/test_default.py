'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.security.roles.default import DefaultRole


class TestDefaultContextSecurity(unittest.TestCase):

    def test_get_context(self):
        default_context = DefaultRole("connection")
        clause = default_context.get_context('tenant', {})
        self.assertIsNone(clause)

    def test_check_context(self):
        default_context = DefaultRole("connection")
        context = default_context.check_context('tenant', {}, [])
        self.assertTrue(context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
