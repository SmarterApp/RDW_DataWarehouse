'''
Created on Jul 16, 2013

@author: tosako
'''
import unittest
from smarter.reports.filters.demographics import getValue, \
    DEMOGRAPHICS_SELECTED_VALUE, getDemographicProgramIepFilter, \
    getDemographicProgram504Filter
from smarter.reports.filters import Constants_filter_names
from smarter.reports.filters.Constants_filter_names import DEMOGRAPHICS_PROGRAM_504, DEMOGRAPHICS_PROGRAM_IEP
from sqlalchemy.sql.expression import true, false


class Test(unittest.TestCase):

    def setUp(self):
        self.test_filter = {}
        self.test_filter1 = {'test': [Constants_filter_names.YES]}
        self.test_filter2 = {'test': [Constants_filter_names.YES, Constants_filter_names.NO]}
        self.test_filter3 = {'test': [Constants_filter_names.YES, Constants_filter_names.NO, Constants_filter_names.NOT_STATED]}

    def test_value_NONE(self):
        rtn_value = getValue(self.test_filter, 'test')
        self.assertTrue(rtn_value == DEMOGRAPHICS_SELECTED_VALUE.NONE)
        rtn_value = getValue(self.test_filter1, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NONE)
        rtn_value = getValue(self.test_filter2, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NONE)
        rtn_value = getValue(self.test_filter3, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NONE)

    def test_value_YES(self):
        rtn_value = getValue(self.test_filter, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.YES)
        rtn_value = getValue(self.test_filter1, 'test')
        self.assertTrue(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.YES)
        rtn_value = getValue(self.test_filter2, 'test')
        self.assertTrue(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.YES)
        rtn_value = getValue(self.test_filter3, 'test')
        self.assertTrue(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.YES)

    def test_value_NO(self):
        rtn_value = getValue(self.test_filter, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NO)
        rtn_value = getValue(self.test_filter1, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NO)
        rtn_value = getValue(self.test_filter2, 'test')
        self.assertTrue(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NO)
        rtn_value = getValue(self.test_filter3, 'test')
        self.assertTrue(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NO)

    def test_value_NOT_STATED(self):
        rtn_value = getValue(self.test_filter, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED)
        rtn_value = getValue(self.test_filter1, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED)
        rtn_value = getValue(self.test_filter2, 'test')
        self.assertFalse(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED)
        rtn_value = getValue(self.test_filter3, 'test')
        self.assertTrue(rtn_value & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED)

    def test_getDemographicProgramIepFilter(self):
        test_filter = {}
        value = getDemographicProgramIepFilter(test_filter)
        self.assertFalse(value)
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES]}
        value = getDemographicProgramIepFilter(test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(type(value[0]), type(true()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NO]}
        value = getDemographicProgramIepFilter(test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(type(value[0]), type(false()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NOT_STATED]}
        value = getDemographicProgramIepFilter(test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(value[0], None)
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, Constants_filter_names.NO, Constants_filter_names.NOT_STATED]}
        value = getDemographicProgramIepFilter(test_filter)
        self.assertEqual(3, len(value))

    def test_getDemographicProgram504Filter(self):
        test_filter = {}
        value = getDemographicProgram504Filter(test_filter)
        self.assertFalse(value)
        test_filter = {DEMOGRAPHICS_PROGRAM_504: [Constants_filter_names.YES]}
        value = getDemographicProgram504Filter(test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(type(value[0]), type(true()))
        test_filter = {DEMOGRAPHICS_PROGRAM_504: [Constants_filter_names.NO]}
        value = getDemographicProgram504Filter(test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(type(value[0]), type(false()))
        test_filter = {DEMOGRAPHICS_PROGRAM_504: [Constants_filter_names.NOT_STATED]}
        value = getDemographicProgram504Filter(test_filter)
        self.assertEqual(1, len(value))
        self.assertEqual(value[0], None)
        test_filter = {DEMOGRAPHICS_PROGRAM_504: [Constants_filter_names.YES, Constants_filter_names.NO, Constants_filter_names.NOT_STATED]}
        value = getDemographicProgram504Filter(test_filter)
        self.assertEqual(3, len(value))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_value_NONE']
    unittest.main()
