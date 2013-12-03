__author__ = 'swimberly'

import unittest
import datetime

from DataGeneration.src.additional_asmt_generator import (month_delta, generate_score_offset, get_cut_points,
                                                          determine_perf_lvl, update_scores, get_header_from_file,
                                                          update_row, create_new_json_file, create_list_of_csv_records,
                                                          read_csv_file, output_data)


class AdditionalAssessmentTest(unittest.TestCase):

    def test_month_delta_future(self):
        date = datetime.date(2013, 12, 25)
        result = month_delta(date, 5)
        expected = datetime.date(2014, 5, 25)
        self.assertEqual(result, expected)

    def test_month_delta_past(self):
        date = datetime.date(2013, 12, 25)
        result = month_delta(date, -3)
        expected = datetime.date(2013, 9, 25)
        self.assertEqual(result, expected)

    def test_month_delta_future_edge(self):
        date = datetime.date(2013, 12, 31)
        result = month_delta(date, 2)
        expected = datetime.date(2014, 2, 28)
        self.assertEqual(result, expected)

    def test_generate_score_offset(self):
        for _ in range(10):
            result = generate_score_offset((1, 15))
            self.assertLessEqual(result, 15)
            self.assertGreaterEqual(result, 1)

    def test_generate_score_offset_2(self):
        result = generate_score_offset((14, 15))
        self.assertLessEqual(result, 15)
        self.assertGreaterEqual(result, 14)

    def test_generate_score_offset_3(self):
        for _ in range(10):
            result = generate_score_offset((-10, -15))
            self.assertLessEqual(result, -10)
            self.assertGreaterEqual(result, -15)

    def test_get_cut_points(self):
        asmt_dict = {
            "overall": {
                "min_score": "1200",
                "max_score": "2400",
            },
            "performance_levels": {
                "level_1": {
                    "name": "Minimal Understanding",
                    "cut_point": "1200"
                },
                "level_2": {
                    "name": "Partial Understanding",
                    "cut_point": "1400"
                },
                "level_3": {
                    "name": "Adequate Understanding",
                    "cut_point": "1800"
                },
                "level_4": {
                    "name": "Thorough Understanding",
                    "cut_point": "2100"
                },
                "level_5": {
                    "name": "",
                    "cut_point": ""
                }
            }
        }
        result = get_cut_points(asmt_dict)
        expected = [1400, 1800, 2100]
        self.assertEqual(result, expected)

    def test_get_cut_points_2(self):
        asmt_dict = {
            "overall": {
                "min_score": "1200",
                "max_score": "2400",
            },
            "performance_levels": {
                "level_1": {
                    "name": "Minimal Understanding",
                    "cut_point": "1200"
                },
                "level_2": {
                    "name": "Partial Understanding",
                    "cut_point": "1400"
                },
                "level_3": {
                    "name": "Adequate Understanding",
                    "cut_point": "1800"
                },
                "level_4": {
                    "name": "Thorough Understanding",
                    "cut_point": "2100"
                },
                "level_5": {
                    "name": "Blah",
                    "cut_point": "2250"
                }
            }
        }
        result = get_cut_points(asmt_dict)
        expected = [1400, 1800, 2100, 2250]
        self.assertEqual(result, expected)

    def test_determine_perf_lvl(self):
        score = 1400
        cutpoints = [1400, 1800, 2100]
        result = determine_perf_lvl(score, cutpoints)
        expected = 2
        self.assertEqual(result, expected)

    def test_determine_perf_lvl_2(self):
        score = 1250
        cutpoints = [1400, 1800, 2100]
        result = determine_perf_lvl(score, cutpoints)
        expected = 1
        self.assertEqual(result, expected)

    def test_determine_perf_lvl_3(self):
        score = 2300
        cutpoints = [1400, 1800, 2100]
        result = determine_perf_lvl(score, cutpoints)
        expected = 4
        self.assertEqual(result, expected)

    def test_determine_perf_lvl_4(self):
        score = 2300
        cutpoints = [1400, 1800, 2100, 2250]
        result = determine_perf_lvl(score, cutpoints)
        expected = 5
        self.assertEqual(result, expected)

    def test_update_scores(self):
        row_dict = {
            'score_asmt': 1500,
            'score_asmt_max': 1525,
            'score_asmt_min': 1475,
            'score_perf_level': 2,
            'score_claim_1': 1499,
            'score_claim_1_max': 1524,
            'score_claim_1_min': 1474,
            'score_claim_2': 1501,
            'score_claim_2_max': 1526,
            'score_claim_2_min': 1476,
            'score_claim_3': 1502,
            'score_claim_3_max': 1527,
            'score_claim_3_min': 1477,
            'score_claim_4': '',
            'score_claim_4_max': '',
            'score_claim_4_min': '',
        }
        cutpoints = [1400, 1800, 2100]
        result = update_scores(row_dict, (-25, -25), cutpoints, 1200, 2400)
        expected = {
            'score_asmt': 1475,
            'score_asmt_max': 1500,
            'score_asmt_min': 1450,
            'score_perf_level': 2,
            'score_claim_1': 1474,
            'score_claim_1_max': 1499,
            'score_claim_1_min': 1449,
            'score_claim_2': 1476,
            'score_claim_2_max': 1501,
            'score_claim_2_min': 1451,
            'score_claim_3': 1477,
            'score_claim_3_max': 1502,
            'score_claim_3_min': 1452,
            'score_claim_4': '',
            'score_claim_4_max': '',
            'score_claim_4_min': '',
        }

        self.assertDictEqual(result, expected)

    def test_update_scores_2(self):
        row_dict = {
            'score_asmt': 1500,
            'score_asmt_max': 1525,
            'score_asmt_min': 1475,
            'score_perf_level': 2,
            'score_claim_1': 1500,
            'score_claim_1_max': 1525,
            'score_claim_1_min': 1475,
            'score_claim_2': 1500,
            'score_claim_2_max': 1525,
            'score_claim_2_min': 1475,
            'score_claim_3': 1500,
            'score_claim_3_max': 1525,
            'score_claim_3_min': 1475,
            'score_claim_4': 1500,
            'score_claim_4_max': 1500,
            'score_claim_4_min': 1500,
        }
        cutpoints = [1400, 1800, 2100]
        result = update_scores(row_dict, (550, 550), cutpoints, 1200, 2400)
        expected = {
            'score_asmt': 2050,
            'score_asmt_max': 2075,
            'score_asmt_min': 2025,
            'score_perf_level': 3,
            'score_claim_1': 2050,
            'score_claim_1_max': 2075,
            'score_claim_1_min': 2025,
            'score_claim_2': 2050,
            'score_claim_2_max': 2075,
            'score_claim_2_min': 2025,
            'score_claim_3': 2050,
            'score_claim_3_max': 2075,
            'score_claim_3_min': 2025,
            'score_claim_4': 2050,
            'score_claim_4_max': 2050,
            'score_claim_4_min': 2050,
        }

        self.assertDictEqual(result, expected)

    def test_update_scores_max(self):
        row_dict = {
            'score_asmt': 2400,
            'score_asmt_max': 2400,
            'score_asmt_min': 2350,
            'score_perf_level': 4,
            'score_claim_1': 2400,
            'score_claim_1_max': 2400,
            'score_claim_1_min': 2350,
            'score_claim_2': 2400,
            'score_claim_2_max': 2400,
            'score_claim_2_min': 2350,
            'score_claim_3': 2350,
            'score_claim_3_max': 2350,
            'score_claim_3_min': 2350,
            'score_claim_4': 2300,
            'score_claim_4_max': 2300,
            'score_claim_4_min': 2300,
        }
        cutpoints = [1400, 1800, 2100]
        result = update_scores(row_dict, (550, 550), cutpoints, 1200, 2400)
        expected = {
            'score_asmt': 2400,
            'score_asmt_max': 2400,
            'score_asmt_min': 2400,
            'score_perf_level': 4,
            'score_claim_1': 2400,
            'score_claim_1_max': 2400,
            'score_claim_1_min': 2400,
            'score_claim_2': 2400,
            'score_claim_2_max': 2400,
            'score_claim_2_min': 2400,
            'score_claim_3': 2400,
            'score_claim_3_max': 2400,
            'score_claim_3_min': 2400,
            'score_claim_4': 2400,
            'score_claim_4_max': 2400,
            'score_claim_4_min': 2400,
        }

        self.assertDictEqual(result, expected)

    def test_update_scores_min(self):
        row_dict = {
            'score_asmt': 1400,
            'score_asmt_max': 1400,
            'score_asmt_min': 1350,
            'score_perf_level': 1,
            'score_claim_1': 1400,
            'score_claim_1_max': 1400,
            'score_claim_1_min': 1350,
            'score_claim_2': 1400,
            'score_claim_2_max': 1400,
            'score_claim_2_min': 1350,
            'score_claim_3': 1350,
            'score_claim_3_max': 1350,
            'score_claim_3_min': 1350,
            'score_claim_4': 1450,
            'score_claim_4_max': 1450,
            'score_claim_4_min': 1450,
        }
        cutpoints = [1400, 1800, 2100]
        result = update_scores(row_dict, (-200, -200), cutpoints, 1200, 2400)
        expected = {
            'score_asmt': 1200,
            'score_asmt_max': 1200,
            'score_asmt_min': 1200,
            'score_perf_level': 1,
            'score_claim_1': 1200,
            'score_claim_1_max': 1200,
            'score_claim_1_min': 1200,
            'score_claim_2': 1200,
            'score_claim_2_max': 1200,
            'score_claim_2_min': 1200,
            'score_claim_3': 1200,
            'score_claim_3_max': 1200,
            'score_claim_3_min': 1200,
            'score_claim_4': 1250,
            'score_claim_4_max': 1250,
            'score_claim_4_min': 1250,
        }

        self.assertDictEqual(result, expected)

    def test_update_row(self):
        pass

    def test_get_header_from_file(self):
        pass

    def test_create_new_json_file(self):
        pass

    def test_create_list_of_csv_records(self):
        pass

    def test_read_csv_file(self):
        pass

    def test_output_data(self):
        pass

if __name__ == '__main__':
    unittest.main()
