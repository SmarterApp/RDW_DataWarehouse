'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.security.context_factory import ContextFactory
from smarter.security.roles.default import append_context
from smarter.security.roles.teacher import append_teacher_context


class TestContextFactory(unittest.TestCase):

    def test_get_context_with_no_role(self):
        context = ContextFactory.get_context("invalid")
        self.assertEqual(context, append_context)

    def test_get_context_with_valid_role(self):
        context = ContextFactory.get_context('TEACHER')
        self.assertEqual(context, append_teacher_context)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
