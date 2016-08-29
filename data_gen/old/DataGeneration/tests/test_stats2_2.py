'''
Created on Apr 19, 2013

@author: kallen
'''
import unittest

import DataGeneration.src.calc.stats as stats


class Test(unittest.TestCase):

    def diff(self, value, vlist):
        dlist = ["%02d" % (abs(v - value) * 100 / value) for v in vlist]
        print("%dif", dlist, "\n")

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
        self.diff(value, out)

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
        self.diff(value, out)

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
        self.diff(value, out)

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
        self.diff(value, out)

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
        self.diff(value, out)

    def test_distribute_by_percentages_06(self):
        value = 1800
        range_min = 1200
        range_max = 2400
        percentages = [0.25, 0.25, 0.25, 0.25]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)
        self.diff(value, out)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
