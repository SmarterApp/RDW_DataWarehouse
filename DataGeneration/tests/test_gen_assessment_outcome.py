import unittest
import gen_assessment_outcome


class TestGenerateData(unittest.TestCase):
    def test_generate_assessment_outcomes(self):
        pass

    def test_get_filtered_assessments(self):
        pass

    def test_create_date_taken_BOY(self):
        year = 2012
        period = 'BOY'
        actual_date = gen_assessment_outcome.create_date_taken(year, period)
        self.assertEqual(actual_date.year, year)
        self.assertTrue(actual_date.month in [9, 10])
        self.assertTrue(actual_date.month in range(1, 29))

    def test_create_date_taken_MOY(self):
        year = 2012
        period = 'MOY'
        actual_date = gen_assessment_outcome.create_date_taken(year, period)
        self.assertTrue(actual_date.month in [11, 12, 1, 2, 3])
        if actual_date.month in [11, 12]:
            self.assertEqual(actual_date.year, year)
        else:
            self.assertEqual(actual_date.year, year + 1)
        self.assertTrue(actual_date.month in range(1, 29))

    def test_create_date_taken_EOY(self):
        year = 2012
        period = 'EOY'
        actual_date = gen_assessment_outcome.create_date_taken(year, period)
        self.assertEqual(actual_date.year, year + 1)
        self.assertTrue(actual_date.month in [4, 5, 6])
        self.assertTrue(actual_date.month in range(1, 29))

    def test_generate_single_assessment_outcome(self):
        pass

    def test_generate_assessment_score(self):
        pass

    def test_calculate_performance_level_boundry_value(self):
        score = 2100
        asmt_cut_point_3 = 2100
        asmt_cut_point_2 = 1800
        asmt_cut_point_1 = 120
        expected_performance_level = 4
        actual_performance_level = gen_assessment_outcome.calculate_performance_level(score, asmt_cut_point_3, asmt_cut_point_2, asmt_cut_point_1)
        self.assertEqual(expected_performance_level, actual_performance_level)

    def test_calculate_performance_level_between_two_levels(self):
        score = 1723
        asmt_cut_point_3 = 2100
        asmt_cut_point_2 = 1800
        asmt_cut_point_1 = 120
        expected_performance_level = 2
        actual_performance_level = gen_assessment_outcome.calculate_performance_level(score, asmt_cut_point_3, asmt_cut_point_2, asmt_cut_point_1)
        self.assertEqual(expected_performance_level, actual_performance_level)

    def test_generate_plus_minus_normal_overall_score(self):
        overall_score = 1912
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_plus_minus = 36
        actual_plus_minus = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(expected_plus_minus, actual_plus_minus)

    def test_generate_plus_minus_small_overall_score(self):
        overall_score = 1201
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_plus_minus = 0
        actual_plus_minus = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(expected_plus_minus, actual_plus_minus)

    def test_generate_plus_minus_high_overall_score(self):
        overall_score = 2390
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_plus_minus = 0
        actual_plus_minus = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(expected_plus_minus, actual_plus_minus)

    # TODO: need to change input parameter: assessment to fields used in this method
    def test_generate_claim_scores(self):
        pass

    def test_rescale_value(self):
        old_value = 245
        old_scale = [50, 500]
        new_scale = [1200, 2400]
        expected_rescaled_value = (old_value - old_scale[0]) * (new_scale[1] - new_scale[0]) / (old_scale[1] - old_scale[0]) + new_scale[0]
        actual_rescaled_value = gen_assessment_outcome.rescale_value(old_value, old_scale, new_scale)
        self.assertEqual(expected_rescaled_value, actual_rescaled_value)

    def test_calculate_claim_average_score(self):
        minimum = 35
        maximum = 90
        expected_claim_average_score = (minimum + maximum) / 2
        actual_claim_average_score = gen_assessment_outcome.calculate_claim_average_score(minimum, maximum)
        self.assertEqual(expected_claim_average_score, actual_claim_average_score)

    def test_calculate_claim_standard_deviation(self):
        average = 45
        minimum = 20
        expected_claim_standard_deviation = (average - minimum) / 4
        actual_claim_standard_deviation = gen_assessment_outcome.calculate_claim_standard_deviation(average, minimum)
        self.assertEqual(expected_claim_standard_deviation, actual_claim_standard_deviation)
