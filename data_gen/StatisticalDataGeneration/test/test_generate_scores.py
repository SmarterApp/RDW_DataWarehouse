import unittest
import generate_scores
import random


class TestGenerateScores(unittest.TestCase):
    '''
    Tests for generate_scores.py
    '''

    def test_add_or_delete_add_more(self):
        score_list = [1, 2, 3, 4, 5, 6]
        required_number = 10
        actual_list = generate_scores.add_or_delete(score_list, required_number)
        self.assertEqual(len(actual_list), required_number)
        self.assertTrue(min(actual_list) >= min(score_list))
        self.assertTrue(max(actual_list) <= max(score_list))

    def test_add_or_delete_delete_more(self):
        score_list = [1, 2, 3, 4, 5, 6, 7]
        required_number = 5
        actual_list = generate_scores.add_or_delete(score_list, required_number)
        self.assertEqual(len(actual_list), required_number)
        self.assertTrue(min(actual_list) >= min(score_list))
        self.assertTrue(max(actual_list) <= max(score_list))

    def test_adjust_list_normal_case(self):
        total = 121
        percentage = [14, 42, 37, 7]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        total_list = random.sample(range(cut_points[0], cut_points[-1] + 1), total)
        actual_scores = generate_scores.adjust_list(total_list, percentage, cut_points, total)
        self.assertEqual(len(actual_scores), total)
        # verify each performance level
        for i in range(len(percentage) - 1):
            expected_number_in_this_range = int(percentage[i] * total / 100)
            actual_number_in_this_level = [x for x in actual_scores if x in range(cut_points[i], cut_points[i + 1])]
            self.assertEqual(len(actual_number_in_this_level), expected_number_in_this_range)

    def test_adjust_list_extream_case(self):
        total = 121
        percentage = [98, 1, 0, 1]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        total_list = random.sample(range(cut_points[0], cut_points[len(cut_points) - 1] + 1), total)
        actual_scores = generate_scores.adjust_list(total_list, percentage, cut_points, total)
        self.assertEqual(len(actual_scores), total)
        # verify each performance level
        for i in range(len(percentage) - 1):
            expected_number_in_this_range = int(percentage[i] * total / 100)
            actual_number_in_this_level = [x for x in actual_scores if x in range(cut_points[i], cut_points[i + 1])]
            self.assertEqual(len(actual_number_in_this_level), expected_number_in_this_range)

    def test_calculate_absolute_values(self):
        percentage = [23, 45, 29, 3]
        total = 1236
        actual_values = generate_scores.calculate_absolute_values(percentage, total)
        self.assertEqual(sum(actual_values), total)
        for i in range(len(percentage) - 1):
            self.assertEqual(actual_values[i], int(total * percentage[i] / 100))

    def test_generate_random_numbers(self):
        min_number = 1200
        max_number = 2400
        count = 400
        actual_numbers = generate_scores.generate_random_numbers(min_number, max_number, count)
        self.assertEqual(len(actual_numbers), count)
        self.assertTrue(min_number <= min(actual_numbers) and max(actual_numbers) <= max_number)

    def test_generate_random_scores(self):
        percentage = [30, 34, 28, 8]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        total = 2000
        actual_scores = generate_scores.generate_random_scores(percentage, cut_points, total)
        for i in range(len(percentage)):
            if i == len(percentage) - 1:
                high_bound = cut_points[i + 1] + 1
            else:
                high_bound = cut_points[i + 1]
            expected_number = int(total * percentage[i] / 100)
            actual_socres_in_level = [x for x in actual_scores if x in range(cut_points[i], high_bound)]
            self.assertEqual(len(actual_socres_in_level), expected_number)

    def test_generate_overall_scores(self):
        percentage = [26, 39, 29, 6]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        total = 12933
        actual_scores = generate_scores.generate_overall_scores(percentage, cut_points, min_score, max_score, total)
        self.assertEqual(len(actual_scores), total)
        # verify each performance level
        for i in range(len(percentage) - 1):
            expected_number_in_this_range = int(percentage[i] * total / 100)
            actual_number_in_this_level = [x for x in actual_scores if x in range(cut_points[i], cut_points[i + 1])]
            self.assertEqual(len(actual_number_in_this_level), expected_number_in_this_range)
        # can add graph display here
