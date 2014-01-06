'''
Created on Apr 15, 2013

@author: kallen
'''
import unittest
from DataGeneration.src.calc.errorband import calc_eb_params, calc_eb, _calc_ebmax


class Test(unittest.TestCase):

    def setUp(self):
        self.smin, self.smax, self.ebmin_divisor, self.ebmax_divisor = 1200, 2400, 32, 8
        self.rndlo, self.rndhi = -10, 25
        self.scenter, self.ebmin, self.ebstep = calc_eb_params(self.smin, self.smax, self.ebmin_divisor, self.ebmax_divisor)
        # the following is only needed to help unut-tests to run
        self.ebmax = _calc_ebmax(self.smin, self.smax, self.ebmax_divisor)

    def tearDown(self):
        pass

    def test_calc_eb_params(self):
        self.assertEqual(self.scenter, 1800)
        self.assertEqual(self.ebmin, 37.5)
        self.assertEqual(self.ebstep, 0.1875)

    def test_calc_ebmax(self):
        self.assertEqual(self.ebmax, 150)

    def test_calc_eb_scenter_no_random(self):
        score = self.scenter
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=True)
        self.assertEqual(ebhalf, self.ebmin)
        self.assertEqual(ebleft, (score - ebhalf))
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, (score + ebhalf))

    def test_calc_eb_smin_no_random(self):
        score = self.smin
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=False)
        self.assertEqual(ebhalf, self.ebmax)
        self.assertEqual(ebleft, self.smin)
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, (score + ebhalf))

    def test_calc_eb_smax_no_random(self):
        score = self.smax
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=False)
        self.assertEqual(ebhalf, self.ebmax)
        self.assertEqual(ebleft, (score - ebhalf))
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, self.smax)

    def test_calc_eb_near_smin_no_random(self):
        score = self.smin + 25
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=False)
        self.assertEqual(ebhalf, 145.3125)
        self.assertEqual(ebleft, self.smin)
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, (score + ebhalf))

    def test_calc_eb_near_smax_no_random(self):
        score = self.smax - 25
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=False)
        self.assertEqual(ebhalf, 145.3125)
        self.assertEqual(ebleft, (score - ebhalf))
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, self.smax)

    def test_calc_eb_using_symmetry_max(self):
        score = self.smax - 25
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=True)
        self.assertEqual(ebhalf, 145.3125)
        self.assertEqual(ebleft, (score - 25))
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, self.smax)

    def test_calc_eb_using_symmetry_min(self):
        score = self.smin + 25
        ebleft, ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, clip_eb=True, ensure_symmetry=True)
        self.assertEqual(ebhalf, 145.3125)
        self.assertEqual(ebleft, self.smin)
        self.assertTrue(ebleft >= self.smin)
        self.assertTrue(ebright <= self.smax)
        self.assertEqual(ebright, (score + 25))

#    def test_calc_eb_scenter_with_random(self):
#        score = self.scenter
#        _ebleft, _ebright, ebhalf = calc_eb(score, self.smin, self.smax, self.scenter, self.ebmin, self.ebstep, self.rndlo, self.rndhi)
#        self.assertEqual(ebhalf, self.ebmin)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
