'''
Created on Apr 17, 2013

@author: swimberly
'''
import unittest
from datetime import date
import generate_data
import generate_entities


class Test(unittest.TestCase):

    def test_calcuate_claim_scores(self):
        assmt = create_assessment()
        res = generate_data.calculate_claim_scores(2105, assmt, 32, 8, -10, 25)
        for claim in res:
            print(claim.claim_score)

    def test_translate_scores_to_assessment_score(self):
        assmt = create_assessment()
        scores = [2180, 1200, 2400, 1590, 1890]
        expected_pl = [4, 1, 4, 2, 3]
        res = generate_data.translate_scores_to_assessment_score(scores, [1575, 1875, 2175], assmt, 32, 8, -10, 25)
        for i in range(len(res)):
            self.assertEqual(res[i].perf_lvl, expected_pl[i])
            self.assertIn(res[i].perf_lvl, [1, 2, 3, 4])

    def test_get_subset_of_students(self):
        students = [object()] * 100
        print(len(students))
        res = generate_data.get_subset_of_students(students, .9)
        self.assertEqual(len(res), 90)


def create_assessment():
    asmts = generate_entities.generate_assessments([5], [1575, 1875, 2175], date.today(), True, date.today())
    return asmts[0]

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
