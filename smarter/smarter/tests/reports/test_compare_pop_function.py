'''
Created on Mar 8, 2013

@author: tosako
'''
import unittest
from smarter.reports.compare_pop_report import Constants


class Test(unittest.TestCase):

    def prepare_total_result(self, seeds):
        total = 0
        intervals = []
        for seed in seeds:
            total = total + seed
            interval = {Constants.COUNT: seed}
            intervals.append(interval)
        total_result = {Constants.TOTAL: total, Constants.INTERVALS: intervals}
        return total_result

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
