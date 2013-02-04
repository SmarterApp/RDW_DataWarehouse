import unittest
import assessment
from constants import MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, ASSMT_TYPES


class TestAssessment(unittest.TestCase):

    def test_generate_assmt_scores_lessthansixgrade(self):
        state = 'Delaware'
        asmt_type = 'Math'
        year = 2011
        period = 'EOY'
        grade = 5
        total = 200

        expected_scorelist = assessment.generate_assmt_scores(state, asmt_type, year, period, grade, total)
        expected_claimnames = ASSMT_TYPES[asmt_type]['4']['claim_names']

        self.assertEqual(len(expected_scorelist), total)
        for score in expected_scorelist:
            self.assertTrue(MIN_ASSMT_SCORE <= score.overall <= MAX_ASSMT_SCORE)
            calculate_overall = sum(score.claims.values())
            self.assertEqual(calculate_overall, score.overall)
            self.assertEqual(sorted(score.claims.keys()), sorted(expected_claimnames))

    def test_generate_assmt_scores_higherthansixgrade(self):
        state = 'Delaware'
        asmt_type = 'ELA'
        year = 2009
        period = 'BOY'
        grade = 11
        total = 1378

        expected_scorelist = assessment.generate_assmt_scores(state, asmt_type, year, period, grade, total)
        expected_claimnames = ASSMT_TYPES[asmt_type]['8']['claim_names']

        self.assertEqual(len(expected_scorelist), total)
        for score in expected_scorelist:
            self.assertTrue(MIN_ASSMT_SCORE <= score.overall <= MAX_ASSMT_SCORE)
            calculate_overall = sum(score.claims.values())
            self.assertEqual(calculate_overall, score.overall)
            self.assertEqual(sorted(score.claims.keys()), sorted(expected_claimnames))


if __name__ == "__main__":
    unittest.main()
