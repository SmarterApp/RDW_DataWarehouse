import unittest
import gen_assessment_outcome


class TestGenerateData(unittest.TestCase):
    def test_generate_assessment_outcomes(self):
        pass

    def test_get_filtered_assessments(self):
        pass

    def test_create_date_taken(self):
        pass

    def test_generate_single_assessment_outcome(self):
        pass

    def test_generate_assessment_score(self):
        pass

    def test_calculate_performance_level(self):
        pass

    def test_generate_plus_minus_normal_overall_score(self):
        overall_score = 1912
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_value = 36
        actual_value = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(actual_value, expected_value)

    # TODO: need to change input parameter: assessment to fields used in this method
    def test_generate_claim_scores(self):
        pass

    def test_rescale_value(self):
        old_value = 245
        old_scale = [50, 500]
        new_scale = [1200, 2400]
        expected_value = (old_value - old_scale[0]) * (new_scale[1] - new_scale[0]) / (old_scale[1] - old_scale[0]) + new_scale[0]
        actual_value = gen_assessment_outcome.rescale_value(old_value, old_scale, new_scale)
        self.assertEqual(expected_value, actual_value)

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
