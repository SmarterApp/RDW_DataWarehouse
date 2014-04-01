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

    def test_generate_data_row_all_nums_gt_zero(self):
        result = generate_data_row(100, 90, 200, 180, 75)

        self.assertEqual(['90', '50', '100', '50', '10', '11.11', '0', '75', '83.33'], result)

    def test_generate_data_row_prev_count_zero(self):
        result = generate_data_row(100, 0, 200, 180, 0)

        self.assertEqual(['0', '0', '100', '50', '100', '', '50', '0', ''], result)

    def test_generate_data_row_prev_total_zero(self):
        result = generate_data_row(100, 0, 200, 0, 0)

        self.assertEqual(['0', '', '100', '50', '100', '', '', '0', ''], result)

    def test_generate_data_row_prev_total_none(self):
        result = generate_data_row(100, None, 200, None, None)

        self.assertEqual(['', '', '100', '50', '', '', '', '', ''], result)
