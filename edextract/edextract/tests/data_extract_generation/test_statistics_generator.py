import unittest
from edextract.data_extract_generation.statistics_generator import (_percentage, generate_data_row, _format_floatval,
                                                                    _format_intval)

__author__ = 'ablum'


class TestStatisticsGenerator(unittest.TestCase):
    def setUp(self):
        pass

    def test__percent(self):
        self.assertEquals(_percentage(50, 100), 50)

    def test__format_floatval_no_decimal(self):
        self.assertEquals(_format_floatval(50.0), '50')

    def test__format_floatval_one_decimal(self):
        self.assertEquals(_format_floatval(50.500), '50.5')

    def test__format_floatval_two_decimal(self):
        self.assertEquals(_format_floatval(50.55), '50.55')

    def test__format_floatval_three_decimal(self):
        self.assertEquals(_format_floatval(50.556), '50.56')

    def test__format_floatval_negative(self):
        self.assertEquals(_format_floatval(-50.556), '-50.56')

    def test__format_floatval_zero(self):
        self.assertEquals(_format_floatval(0.0), '0')

    def test__format_floatval_none(self):
        self.assertEquals(_format_floatval(None), '')

    def test__format_intval_positive(self):
        self.assertEquals(_format_intval(10), '10')

    def test__format_intval_negative(self):
        self.assertEquals(_format_intval(-10), '-10')

    def test__format_intval_zero(self):
        self.assertEquals(_format_intval(0), '0')

    def test__format_intval_none(self):
        self.assertEquals(_format_intval(None), '')

    def test_generate_data_row(self):
        current_year_count = 100
        previous_year_count = 90
        current_year_total = 200
        previous_year_total = 180

        result = generate_data_row(current_year_count, previous_year_count,
                                   current_year_total, previous_year_total)

        self.assertEquals(len(result), 7)

        self.assertEquals(result[0], '90')
        self.assertEquals(result[1], '50')
        self.assertEquals(result[2], '100')
        self.assertEquals(result[3], '50')
        self.assertEquals(result[4], '10')
        self.assertEquals(result[5], '11.11')
        self.assertEquals(result[6], '0')
