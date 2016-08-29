'''
Created on Apr 19, 2013

@author: kallen
'''
import unittest

import DataGeneration.src.calc.stats as stats


class Test(unittest.TestCase):

    def test_weighted_sum_01(self):
        values = [100]
        percentages = [.10]
        out = stats.weighted_sum(values, percentages)
        self.assertEqual(10, out)

    def test_weighted_sum_02(self):
        values = [100, 200]
        percentages = [.10, .20]
        out = stats.weighted_sum(values, percentages)
        self.assertEqual(50, out)

    def test_weighted_sum_03(self):
        values = [100, 200]
        percentages = [.20, .10]
        out = stats.weighted_sum(values, percentages)
        self.assertEqual(40, out)

    def test_random_split_01(self):
        val = 99
        out = stats._random_split(val, 3)
        self.assertEqual(val, sum(out))

    def test_random_split_02(self):
        val = 100
        out = stats._random_split(val, 3)
        self.assertEqual(val, sum(out))

    def test_random_split_03(self):
        val = -99
        out = stats._random_split(val, 3)
        self.assertEqual(val, sum(out))

    def test_random_split_04(self):
        val = -100
        out = stats._random_split(val, 3)
        self.assertEqual(val, sum(out))

    def test_random_split_05(self):
        val = 99
        out = stats._random_split(val, 4)
        self.assertEqual(val, sum(out))

    def test_random_split_06(self):
        val = 100
        out = stats._random_split(val, 4)
        self.assertEqual(val, sum(out))

    def test_random_split_07(self):
        val = -99
        out = stats._random_split(val, 4)
        self.assertEqual(val, sum(out))

    def test_random_split_08(self):
        val = -100
        out = stats._random_split(val, 4)
        self.assertEqual(val, sum(out))

    def test_zero_sum_list_01(self):
        val = 99
        out = stats._zero_sum_split(val, 3)
        self.assertEqual(sum(out), 0)

    def test_zero_sum_list_02(self):
        val = 100
        out = stats._zero_sum_split(val, 3)
        self.assertEqual(sum(out), 0)

    def test_zero_sum_list_03(self):
        val = 99
        out = stats._zero_sum_split(val, 4)
        self.assertEqual(sum(out), 0)

    def test_zero_sum_list_04(self):
        val = 100
        out = stats._zero_sum_split(val, 4)
        self.assertEqual(sum(out), 0)

    def test_scaled_up_01(self):
        val = 1000
        percentages = [0.99, 0.01]
        need = len(percentages)
        list1 = stats._zero_sum_split(val, need)
        self.assertEqual(sum(list1), 0)
        list2 = stats._scaled_up(list1, percentages)
        ws = stats.weighted_sum(list2, percentages)
        self.assertTrue(stats.approx_equal(ws, 0, 1))

    def test_scaled_up_02(self):
        val = 1000
        percentages = [0.8, 0.1, 0.1]
        need = len(percentages)
        list1 = stats._zero_sum_split(val, need)
        self.assertEqual(sum(list1), 0)
        list2 = stats._scaled_up(list1, percentages)
        ws = stats.weighted_sum(list2, percentages)
        self.assertTrue(stats.approx_equal(ws, 0, 1))

    def test_approx_equal_01(self):
        x = .9991
        y = .9992
        out = stats.approx_equal(x, y, 1e-2, True)
        self.assertTrue(out)

    def test_approx_equal_02(self):
        x = .9991
        y = .9992
        out = stats.approx_equal(x, y, 1e-3, True)
        self.assertTrue(out)

    def test_approx_equal_03(self):
        x = .9991
        y = .9992
        out = stats.approx_equal(x, y, 1e-4, True)
        self.assertTrue(out)

    def test_approx_equal_04(self):
        x = .9991
        y = .9992
        out = stats.approx_equal(x, y, 1e-5, True)
        self.assertFalse(out)

    def test_approx_equal_05(self):
        x = .8881
        y = .8882
        out = stats.approx_equal(x, y, 1e-5, False)
        self.assertFalse(out)

    def test_distribute_by_percentages_01(self):
        value = 1800
        range_min = 1200
        range_max = 2400
        percentages = [0.7, 0.1, 0.1, 0.1]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)

    def test_distribute_by_percentages_02(self):
        value = 1800
        range_min = 1200
        range_max = 2400
        percentages = [0.85, 0.05, 0.05, 0.05]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)

    def test_distribute_by_percentages_03(self):
        value = 1300
        range_min = 1200
        range_max = 2400
        percentages = [0.85, 0.05, 0.05, 0.05]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)

    def test_distribute_by_percentages_04(self):
        value = 1260
        range_min = 1200
        range_max = 2400
        percentages = [0.85, 0.05, 0.05, 0.05]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)

    def test_distribute_by_percentages_05(self):
        value = 1250
        range_min = 1200
        range_max = 2400
        percentages = [0.85, 0.05, 0.05, 0.05]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
