import unittest
import calculate_statistics
from queries import *
from constants import SCHOOL_LEVELS_INFO


class TestGenerateData(unittest.TestCase):

    def test_get_row(self):
        db_result = [[1, 100],
                     [29, 90]
                     ]
        generated_rows = calculate_statistics.get_rows(db_result)
        self.assertEqual(generated_rows, [1, 29])

    def test_get_statistic3(self):
        generated_stat = calculate_statistics.get_statistic3(mock_get_states_onestate, mock_execute_queries)
        expected_stat = [['DE', 'Delaware', 3, 7, 106, 10, 2, 3, 0.4714045207910317, 2.3333333333333335, 10, 23, 4.2378277069118075, 16.571428571428573, 9.2, 25.9, 6.400637723329303, 16.557142857142857, 0.42857142857142855, 0.2857142857142857, 0.14285714285714285, 0.14285714285714302]]
        self.assertEqual(generated_stat, expected_stat)


def mock_get_states_onestate():
    states = [['Delaware', 'DE', 4]]
    return states


def mock_execute_queries(state_name, query1, query2, para1=None, query3=None):

    # case 1: total district
    if(query1 == query_stat1 and query2 == query_stat2):
        return [3]

    # case 2: total school
    if(query1 == query_stat3 and query2 == query_stat4):
        return [7]

    # case 3: total student
    if(query1 == query_stat9 and query2 == query_stat10):
        return [106]

    # case 4: total teachers
    if(query1 == query_stat11 and query2 == query_stat12):
        return [10]

    # case 5: school_num_in_dist
    if(query1 == query2_first and query2 == query2_second):
        return [2, 2, 3]

    # case 6: stu_num_in_school
    if(query1 == query_stat5 and query2 == query_stat6):
        return [15, 10, 23, 12, 19, 20, 17]

    # case 7: stutea_ratio_in_school
    if(query1 == query_stat7 and query2 == query_stat8):
        return [10.1, 10, 19.8, 25.9, 17.3, 9.2, 23.6]

    # case 8: school_types
    if(query1 == query_stat13 and query2 == query_stat14 and query3 == query_stat15):
        if(para1 == SCHOOL_LEVELS_INFO[0][0]):
            return [3]
        if(para1 == SCHOOL_LEVELS_INFO[1][0]):
            return [2]
        if(para1 == SCHOOL_LEVELS_INFO[2][0]):
            return [1]
        if(para1 == SCHOOL_LEVELS_INFO[3][0]):
            return [1]

if __name__ == "__main__":
    unittest.main()
