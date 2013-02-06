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

    # test generate_allscores()
    def test_generate_allscores(self):
        score_list = [387, 381, 276, 488, 123, 298]
        levels = []
        asmt_type = 'ELA'
        grade = '4'

        generated_allscores = assessment.generate_allscores(score_list, levels, asmt_type, grade)

        self.assertEqual(len(generated_allscores), len(score_list))
        for i in range(len(generated_allscores)):
            self.assertEqual(generated_allscores[i].overall, score_list[i])

    # test generate_claims(total_score, asmt_type, grade)
    def test_generate_claims(self):
        total_score = []
        asmt_type = 'Math'
        grade = '4'

    # test perc_to_count(perc, total)
    def test_perc_to_count1(self):
        perc = [40, 35, 10, 15]
        total = 548

        generated_counts = assessment.perc_to_count(perc, total)
        self.assertEqual(generated_counts, [219, 192, 55, 82])

    def test_perc_to_count2(self):
        perc = [40, 35, 10, 15]
        total = 56

        generated_counts = assessment.perc_to_count(perc, total)
        self.assertEqual(generated_counts, [22, 20, 6, 8])

if __name__ == "__main__":
    unittest.main()
