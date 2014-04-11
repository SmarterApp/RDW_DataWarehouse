__author__ = 'tshewchuk'

"""
Module containing data_generator_helper unit tests.
"""

import unittest
from edextract.data_extract_generation.data_generator_helper import percentage, subtract, format_intval, format_floatval


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
