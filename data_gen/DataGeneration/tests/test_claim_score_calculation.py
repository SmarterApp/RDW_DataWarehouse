__author__ = 'sravi'

import unittest
import DataGeneration.src.calc.claim_score_calculation as claim_score_calculation


class TestClaimScoreCalc(unittest.TestCase):
    '''
    Tests for claim score calculation
    '''

    def test_claim_perf_level_calc_level_1(self):
        cut_points = [1600, 2000]
        claim_scores = [1200, 1201, 1400, 1600, 1601, 2000, 2002, 2400]
        expected_claim_perf_lvl = [1, 1, 1, 2, 2, 3, 3, 3]

        for i in range(len(claim_scores)):
            perl_lvl = claim_score_calculation.determine_claim_perf_level(claim_scores[i], cut_points)
            self.assertEqual(expected_claim_perf_lvl[i], perl_lvl)
