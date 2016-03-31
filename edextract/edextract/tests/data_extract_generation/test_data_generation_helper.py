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

__author__ = 'tshewchuk'

"""
Module containing data_generator_helper unit tests.
"""

import unittest
from edextract.data_extract_generation.data_generator_helper import (percentage, subtract, format_intval, format_floatval,
                                                                     get_row_identifiers)
from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgNameKey
from edextract.trackers.program_tracker import LEPStatusTracker


class TestDataGenerationHelper(unittest.TestCase):

    def setUp(self):
        pass

    def test_percent(self):
        self.assertEquals(percentage(50, 100), 50)

    def test_percent_of_zero(self):
        self.assertEquals(percentage(50, 0), None)

    def test_percent_of_none(self):
        self.assertEquals(percentage(50, None), None)

    def test_subtract(self):
        self.assertEquals(subtract(100, 50), 50)

    def test_subtract_negative(self):
        self.assertEquals(subtract(50, 100), -50)

    def test_subtract_none(self):
        self.assertEquals(subtract(100, None), None)

    def test_subtract_float(self):
        self.assertEquals(subtract(.75, .5), .25)

    def test_format_floatval_no_decimal(self):
        self.assertEquals(format_floatval(50.0), '50')

    def test_format_floatval_one_decimal(self):
        self.assertEquals(format_floatval(50.500), '50.5')

    def test_format_floatval_two_decimal(self):
        self.assertEquals(format_floatval(50.55), '50.55')

    def test_format_floatval_three_decimal(self):
        self.assertEquals(format_floatval(50.556), '50.56')

    def test_format_floatval_negative(self):
        self.assertEquals(format_floatval(-50.556), '-50.56')

    def test_format_floatval_zero(self):
        self.assertEquals(format_floatval(0.0), '0')

    def test_format_floatval_none(self):
        self.assertEquals(format_floatval(None), '')

    def test_format_intval_positive(self):
        self.assertEquals(format_intval(10), '10')

    def test_format_intval_negative(self):
        self.assertEquals(format_intval(-10), '-10')

    def test_format_intval_zero(self):
        self.assertEquals(format_intval(0), '0')

    def test__format_intval_none(self):
        self.assertEquals(format_intval(None), '')

    def test_get_row_identifiers(self):
        # New Jersey state Central Regional district LEP Status row.
        key = EdOrgNameKey(state_name='New Jersey', district_name='Central Regional', school_name='')
        tracker = LEPStatusTracker()
        state_name, district_name, school_name, category, value = get_row_identifiers(key, tracker)

        self.assertEqual('New Jersey', state_name)
        self.assertEqual('Central Regional', district_name)
        self.assertEqual('ALL', school_name)
        self.assertEqual('Program', category)
        self.assertEqual('LEPStatus', value)
