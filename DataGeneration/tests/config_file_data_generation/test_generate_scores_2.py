'''
Created on Apr 15, 2013

@author: kallen
'''
import unittest
from config_file_data_generation.generate_scores import split_total_by_precentages, \
    generate_random_scores_by_percentage_between_cut_points, generate_overall_scores
    


class Test(unittest.TestCase):


    def test_split_by_percentages_1(self):
        percentages = [10, 20, 30, 40]
        total = 100
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 10)
        self.assertEqual(output[1], 20)
        self.assertEqual(output[2], 30)
        self.assertEqual(output[3], 40)
        
    def test_split_by_percentages_2(self):
        percentages = [10, 20, 30, 40]
        total = 1000
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 100)
        self.assertEqual(output[1], 200)
        self.assertEqual(output[2], 300)
        self.assertEqual(output[3], 400)
  
        
    def test_split_by_percentages_3(self):
        percentages = [30, 34, 28, 9]
        total = 15
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 4)
        self.assertEqual(output[1], 5)
        self.assertEqual(output[2], 4)
        self.assertEqual(output[3], 2)
  
        
    def test_split_by_percentages_4(self):
        percentages = [30, 34, 28, 9]
        total = 60
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 18)
        self.assertEqual(output[1], 20)
        self.assertEqual(output[2], 16)
        self.assertEqual(output[3], 6)
        
    
    def test_split_by_percentages_5(self):
        percentages = [30, 40, 30, 0]
        total = 10
        output = split_total_by_precentages(percentages, total)
        self.assertEqual(output[0], 3)
        self.assertEqual(output[1], 4)
        self.assertEqual(output[2], 3)
        self.assertEqual(output[3], 0)
        
        
    def test_01(self):
        total = 254565
        percentages = [33, 33, 34, 0]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(percentages, cut_points, total)
        count = len(generated_random_numbers)
        self.assertEqual(total, count)
  
        
    def test_02(self):
        total = 10
        percentages = [70, 20, 10, 0]
        cut_points = [1200, 1575, 1875, 2175, 2400]
        min_score = cut_points[0]
        max_score = cut_points[-1]
        generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(percentages, cut_points, total)
        count = len(generated_random_numbers)
        self.assertEqual(total, count)
        
        total_count_by_percentages = split_total_by_precentages(percentages, total)
        print(total_count_by_percentages)
        
        final_scores_list = generate_overall_scores(percentages, cut_points, min_score, max_score, total)
        count = len(final_scores_list)
        self.assertEqual(total, count)
        

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()