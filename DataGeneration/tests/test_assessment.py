from mock import MagicMock

from constants import MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, ASSMT_TYPES
from datetime import date
import assessment
import entities
import unittest
import helper_entities


class TestAssessment(unittest.TestCase):

    def test_generate_assmt_scores_lessthansixgrade(self):
        state = 'Delaware'
        asmt_type = 'Math'
        year = 2011
        period = 'EOY'
        grade = 5
        total = 200

        expected_scorelist = assessment.generate_assmt_scores(state, asmt_type, year, period, grade, total)

        self.assertEqual(len(expected_scorelist), total)
        for score in expected_scorelist:
            self.assertTrue(MIN_ASSMT_SCORE <= score.overall <= MAX_ASSMT_SCORE)
            calculate_overall = sum(score.claims)
            self.assertEqual(calculate_overall, score.overall)

    def test_generate_assmt_scores_higherthansixgrade(self):
        state = 'Delaware'
        asmt_type = 'ELA'
        year = 2009
        period = 'BOY'
        grade = 11
        total = 1378

        state_data = assessment.StateData()
        state_data.get_state_data = MagicMock(return_value=(284, 32, [25, 44, 26, 6]))
        expected_scorelist = assessment.generate_assmt_scores(state, asmt_type, year, period, grade, total)

        self.assertEqual(len(expected_scorelist), total)
        for score in expected_scorelist:
            self.assertTrue(MIN_ASSMT_SCORE <= score.overall <= MAX_ASSMT_SCORE)
            calculate_overall = sum(score.claims)
            self.assertEqual(calculate_overall, score.overall)

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

    def test_generate_assmt_scores_for_subject(self):
        asmt1 = entities.Assessment(897, '897', 'SUMMATIVE', 'EOY', 2010, 'V1', 10, 'Math', '2012-09-10')
        asmt2 = entities.Assessment(898, '898', 'SUMMATIVE', 'EOY', 2010, 'V1', 10, 'ELA', '2012-09-10')
        asmt3 = entities.Assessment(899, '899', 'ITERATIVE', 'BOY', 2010, 'V1', 10, 'Math', '2012-09-10')
        asmt_list = [asmt1, asmt2, asmt3]
        subject_name = 'Math'
        res = assessment.generate_assmt_scores_for_subject(30, 10, 'Delaware', asmt_list, subject_name)

        self.assertEqual(len(res), 2)
        # key1 = '%d_%d' % (date.today().year, asmt1.asmt_id)
        # key3 = '%d_%d' % (date.today().year, asmt3.asmt_id)
        key4 = '%d_%d' % (date.today().year - 1, asmt1.asmt_id)
        key6 = '%d_%d' % (date.today().year - 1, asmt3.asmt_id)
        # self.assertEqual(len(res[key1]), 30)
        # self.assertEqual(len(res[key3]), 30)
        self.assertEqual(len(res[key4]), 30)
        self.assertEqual(len(res[key6]), 30)

        key_list = [key4, key6]
        for key in key_list:
            for score in res[key]:
                self.assertIsInstance(score, helper_entities.Score)

if __name__ == "__main__":
    unittest.main()
