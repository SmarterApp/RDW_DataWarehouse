'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.security.roles.default import DefaultRole


class TestDefaultContextSecurity(unittest.TestCase):

    def test_get_context(self):
        default_context = DefaultRole("connection")
        clause = default_context.get_context('123')
        self.assertIsNone(clause)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
