'''
Created on Apr 15, 2013

@author: kallen
'''
import unittest
from DataGeneration.src.generators.generate_scores import split_total_by_precentages, \
    generate_random_scores_by_percentage_between_cut_points, generate_overall_scores


class Test(unittest.TestCase):

    def test_split_by_percentages_1(self):
        percentages = [10, 20, 30, 40]
        total = 100
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 10)
        self.assertEqual(output[1], 20)
        self.assertEqual(output[2], 30)
        self.assertEqual(output[3], 40)

    def test_split_by_percentages_2(self):
        percentages = [10, 20, 30, 40]
        total = 1000
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 100)
        self.assertEqual(output[1], 200)
        self.assertEqual(output[2], 300)
        self.assertEqual(output[3], 400)

    def test_split_by_percentages_3(self):
        percentages = [30, 34, 28, 9]
        total = 15
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 4)
        self.assertEqual(output[1], 6)
        self.assertEqual(output[2], 4)
        self.assertEqual(output[3], 1)

    def test_split_by_percentages_4(self):
        percentages = [30, 34, 28, 9]
        total = 60
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 18)
        self.assertEqual(output[1], 21)
        self.assertEqual(output[2], 16)
        self.assertEqual(output[3], 5)

    def test_split_by_percentages_5(self):
        percentages = [30, 40, 30, 0]
        total = 10
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 3)
        self.assertEqual(output[1], 4)
        self.assertEqual(output[2], 3)
        self.assertEqual(output[3], 0)

    def test_split_by_percentages_6(self):
        percentages = [26, 26, 47, 1]
        total = 10
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 2)
        self.assertEqual(output[1], 2)
        self.assertEqual(output[2], 6)
        self.assertEqual(output[3], 0)

    def test_01(self):
        total = 254565
        percentages = [84006, 84006, 86553, 0]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(percentages, cut_points, total)
        count = len(generated_random_numbers)
        self.assertEqual(total, count)

    def test_02(self):
        total = 10
        counts = [7, 2, 1, 0]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(counts, cut_points, total)
        count = len(generated_random_numbers)
        self.assertEqual(total, count)

        total_count_by_percentages = split_total_by_precentages(counts, total)
        new_total = sum(total_count_by_percentages)
        self.assertEqual(total, new_total)

        final_scores_list = generate_overall_scores(counts, cut_points, min_score, max_score, total)
        count = len(final_scores_list)
        self.assertEqual(total, count)

    def test_03(self):
        total = 10
        percentages = [7, 3, 0, 0]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(percentages, cut_points, total)
        count = len(generated_random_numbers)
        self.assertEqual(total, count)

        total_count_by_percentages = split_total_by_precentages(percentages, total)
        new_total = sum(total_count_by_percentages)
        self.assertEqual(total, new_total)

        final_scores_list = generate_overall_scores(percentages, cut_points, min_score, max_score, total)
        count = len(final_scores_list)
        self.assertEqual(total, count)

    def test_04(self):
        percentages = [20, 40, 30, 10]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        total = 12933
        actual_scores = generate_overall_scores(percentages, cut_points, min_score, max_score, total)
        self.assertEqual(len(actual_scores), total)

        pl_counts = split_total_by_precentages(percentages, total)
        generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(pl_counts, cut_points, total)
        count = len(generated_random_numbers)
        self.assertEqual(total, count)

        total_count_by_percentages = split_total_by_precentages(pl_counts, total)
        new_total = sum(total_count_by_percentages)
        self.assertEqual(total, new_total)

        final_scores_list = generate_overall_scores(percentages, cut_points, min_score, max_score, total)
        count = len(final_scores_list)
        self.assertEqual(total, count)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
