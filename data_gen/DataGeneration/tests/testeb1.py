'''
Created on Apr 15, 2013

@author: kallen
'''
import unittest
from DataGeneration.src.calc.errorband import calc_eb_params, calc_eb


class Test(unittest.TestCase):

    def test_calc_eb_params(self):
        smin, smax, ebmin_divisor, ebmax_divisor = 1200, 2400, 32, 8
        scenter, ebmin, ebstep = calc_eb_params(smin, smax, ebmin_divisor, ebmax_divisor)
        self.assertEqual(scenter, 1800)
        self.assertEqual(ebmin, 37.5)
        self.assertEqual(ebstep, 0.1875)

    def test_calc_eb_no_random_no_clip(self):
        smin, smax, ebmin_divisor, ebmax_divisor = 1200, 2400, 32, 8
        scenter, ebmin, ebstep = calc_eb_params(smin, smax, ebmin_divisor, ebmax_divisor)

        score = 1800
        ebleft, ebright, ebhalf = calc_eb(score, smin, smax, scenter, ebmin, ebstep)
        self.assertEqual(ebhalf, ebmin)
        self.assertEqual(ebleft, (score - ebmin))
        self.assertEqual(ebright, (score + ebmin))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
