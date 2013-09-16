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

    def doit_01(self, value):
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

    def doit_02(self, value):
        range_min = 1200
        range_max = 2400
        percentages = [0.4, 0.3, 0.2, 0.1]
        out = stats.distribute_by_percentages(value, range_min, range_max, percentages)
        print(value, out)
        ws = stats.weighted_sum(out, percentages)
        self.assertTrue(stats.approx_equal(ws, value, 1))
        for v in out:
            self.assertGreaterEqual(v, range_min)
            self.assertLessEqual(v, range_max)
        self.diff(value, out)

    def test_distribute_by_percentages_01(self):
        for v in range(1200, 2401, 100):
            self.doit_01(v)

    def test_distribute_by_percentages_02(self):
        for v in range(1200, 2401, 100):
            self.doit_02(v)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
