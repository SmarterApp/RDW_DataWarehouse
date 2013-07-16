'''
Created on Jul 16, 2013

@author: tosako
'''
import unittest
from smarter.reports.filters import Constants_filter_names
from smarter.reports.filters.Constants_filter_names import DEMOGRAPHICS_PROGRAM_IEP
from sqlalchemy.sql.expression import true, false
from smarter.reports.filters.demographics import getDemographicFilter


class Test(unittest.TestCase):

    def test_getDemographicProgramFilter(self):
        test_filter = {}
        value = getDemographicFilter(DEMOGRAPHICS_PROGRAM_IEP, test_filter)
        self.assertFalse(value)
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES]}
        value = getDemographicFilter(DEMOGRAPHICS_PROGRAM_IEP, test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(type(value[0]), type(true()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NO]}
        value = getDemographicFilter(DEMOGRAPHICS_PROGRAM_IEP, test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(type(value[0]), type(false()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NOT_STATED]}
        value = getDemographicFilter(DEMOGRAPHICS_PROGRAM_IEP, test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(value[0], None)
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, Constants_filter_names.NO, Constants_filter_names.NOT_STATED]}
        value = getDemographicFilter(DEMOGRAPHICS_PROGRAM_IEP, test_filter)
        self.assertEqual(3, len(value))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, 'whatever']}
        value = getDemographicFilter(DEMOGRAPHICS_PROGRAM_IEP, test_filter)
        self.assertEqual(1, len(value))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_value_NONE']
    unittest.main()
