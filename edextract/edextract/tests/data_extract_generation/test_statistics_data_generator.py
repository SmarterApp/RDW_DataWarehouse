import unittest
from edextract.data_extract_generation.statistics_data_generator import _percentage, generate_data_row

__author__ = 'ablum'


class TestStatisticsDataGenerator(unittest.TestCase):
    def setUp(self):
        pass

    def test__percent(self):
        self.assertEquals(_percentage(50, 100), 50)

    def test_generate_data_row(self):
        current_year_count = 100
        previous_year_count = 90
        current_year_total = 200
        previous_year_total = 180

        result = generate_data_row(current_year_count, previous_year_count,
                                   current_year_total, previous_year_total)

        self.assertEquals(len(result), 7)

        self.assertEquals(result[0], previous_year_count)
        self.assertEquals(result[1], 50)
        self.assertEquals(result[2], current_year_count)
        self.assertEquals(result[3], 50)
        self.assertEquals(result[4], 10)
        self.assertEquals(result[5], 11.11)
        self.assertEquals(result[6], 0)
