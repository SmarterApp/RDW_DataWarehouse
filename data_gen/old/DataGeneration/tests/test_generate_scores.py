import unittest
import DataGeneration.src.generators.generate_scores as generate_scores


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

#    def test_adjust_list_normal_case(self):
#        total = 121
#        percentage = [14, 42, 37, 7]
#        cut_points = [1200, 1575, 1875, 2175, 2400]
#        total_list = random.sample(range(cut_points[0], cut_points[-1] + 1), total)
#        actual_scores = generate_scores.adjust_list(total_list, percentage, cut_points, total)
#        self.assertEqual(len(actual_scores), total)
#        # verify each performance level
#        for i in range(len(percentage) - 1):
#            expected_number_in_this_range = int(percentage[i] * total / 100)
#            actual_number_in_this_level = [x for x in actual_scores if x in range(cut_points[i], cut_points[i + 1])]
#            self.assertEqual(len(actual_number_in_this_level), expected_number_in_this_range)

#    def test_adjust_list_extream_case(self):
#        total = 121
#        percentage = [98, 1, 0, 1]
#        cut_points = [1200, 1575, 1875, 2175, 2400]
#        total_list = random.sample(range(cut_points[0], cut_points[len(cut_points) - 1] + 1), total)
#        actual_scores = generate_scores.adjust_list(total_list, percentage, cut_points, total)
#        self.assertEqual(len(actual_scores), total)
#        # verify each performance level
#        for i in range(len(percentage) - 1):
#            expected_number_in_this_range = int(percentage[i] * total / 100)
#            actual_number_in_this_level = [x for x in actual_scores if x in range(cut_points[i], cut_points[i + 1])]
#            self.assertEqual(len(actual_number_in_this_level), expected_number_in_this_range)

#    def test_calculate_absolute_values(self):
#        percentage = [23, 45, 29, 3]
#        total = 1236
#        actual_values = generate_scores.split_total_by_precentages(percentage, total)
#        self.assertEqual(sum(actual_values), total)
#        for i in range(len(percentage) - 1):
#            self.assertEqual(actual_values[i], int(total * percentage[i] / 100))

    def test_generate_random_numbers(self):
        min_number = 1200
        max_number = 2400
        count = 400
        actual_numbers = generate_scores.generate_random_numbers(min_number, max_number, count)
        self.assertEqual(len(actual_numbers), count)
        self.assertTrue(min_number <= min(actual_numbers) and max(actual_numbers) <= max_number)

    def test_generate_random_scores(self):
        counts = [600, 680, 560, 160]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        total = 2000
        actual_scores = generate_scores.generate_random_scores_by_percentage_between_cut_points(counts, cut_points, total)
        for i in range(len(counts)):
            if i == len(counts) - 1:
                high_bound = cut_points[i + 1] + 1
            else:
                high_bound = cut_points[i + 1]
            expected_number = counts[i]
            actual_socres_in_level = [x for x in actual_scores if x in range(cut_points[i], high_bound)]
            self.assertEqual(len(actual_socres_in_level), expected_number)

    def is_close(self, a, b, diff):
        if a == b:
            return True
        if a < b:
            return a >= b - diff
        # a > b
        return a <= b + diff

    def test_generate_overall_scores_percentage(self):
        percentage = [20, 40, 30, 10]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        total = 12933
        actual_scores = generate_scores.generate_overall_scores(percentage, cut_points, min_score, max_score, total)
        self.assertEqual(len(actual_scores), total)

        total_count_by_percentages = generate_scores.split_total_by_precentages(percentage, total)
        new_total = sum(total_count_by_percentages)
        self.assertEqual(total, new_total)

        cp1min, cp1max = cut_points[0], cut_points[1]
        cp2min, cp2max = cut_points[1], cut_points[2]
        cp3min, cp3max = cut_points[2], cut_points[3]
        cp4min, cp4max = cut_points[3], cut_points[4] + 1

        count1 = len(actual_scores)

        pl1 = [x for x in actual_scores if x in range(cp1min, cp1max)]
        pl2 = [x for x in actual_scores if x in range(cp2min, cp2max)]
        pl3 = [x for x in actual_scores if x in range(cp3min, cp3max)]
        pl4 = [x for x in actual_scores if x in range(cp4min, cp4max)]

        pllist = [len(pl1), len(pl2), len(pl3), len(pl4)]
        count2 = sum(pllist)

        self.assertEqual(count1, count2)

        pl1pc = int((len(pl1) / count1) * 100)
        pl2pc = int((len(pl2) / count1) * 100)
        pl3pc = int((len(pl3) / count1) * 100)
        pl4pc = int((len(pl4) / count1) * 100)

        pclist = [pl1pc, pl2pc, pl3pc, pl4pc]

        for i in range(len(pclist)):
            pc = pclist[i]
            self.assertTrue(self.is_close(pc, percentage[i], 1))

        # can add graph display here

    def test_generate_overall_scores_counts(self):
        counts = [2586, 5173, 3720, 1454]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        total = 12933
        actual_scores = generate_scores.generate_overall_scores(counts, cut_points, min_score, max_score, total, is_percentage=False)
        self.assertEqual(len(actual_scores), total)

        cp1min, cp1max = cut_points[0], cut_points[1]
        cp2min, cp2max = cut_points[1], cut_points[2]
        cp3min, cp3max = cut_points[2], cut_points[3]
        cp4min, cp4max = cut_points[3], cut_points[4] + 1

        count1 = len(actual_scores)

        pl1 = [x for x in actual_scores if x in range(cp1min, cp1max)]
        pl2 = [x for x in actual_scores if x in range(cp2min, cp2max)]
        pl3 = [x for x in actual_scores if x in range(cp3min, cp3max)]
        pl4 = [x for x in actual_scores if x in range(cp4min, cp4max)]
        expected_total = len(actual_scores)

        self.assertEqual(len(pl1), counts[0])
        self.assertEqual(len(pl2), counts[1])
        self.assertEqual(len(pl3), counts[2])
        self.assertEqual(len(pl4), counts[3])
        self.assertEqual(total, expected_total)
