'''
Created on Aug 6, 2013

@author: swimberly
'''
import generate_data_2 as gd2
import helper_entities as he
import unittest


class Test(unittest.TestCase):

    def test_generate_students_with_demographics(self):
        score_pool = {1: [x for x in range(100)], 2: [x for x in range(100)],
                      3: [x for x in range(100)], 4: [x for x in range(100)]}
        demographic_totals = {'male': [1, 20, 5, 5, 5, 5],
                              'female': [1, 24, 6, 6, 6, 6],
                              'not specified': [1, 28, 7, 7, 7, 7],
                              'dmg_eth_ami': [2, 28, 7, 7, 7, 7],
                              'dmg_eth_blk': [2, 24, 6, 6, 6, 6]}
        grade = 3
        results = gd2.generate_students_with_demographics(score_pool, demographic_totals, grade)
        self.assertEquals(len(results), 4)

    def test_assign_demographics_for_grouping(self):
        group_num = 1
        student_info_pool = {1: [he.StudentInfo(3, 'male', 12) for _i in range(50)],
                             2: [he.StudentInfo(3, 'male', 12) for _i in range(50)],
                             3: [he.StudentInfo(3, 'male', 12) for _i in range(50)],
                             4: [he.StudentInfo(3, 'male', 12) for _i in range(50)]}
        demographic_totals = {'dmg_eth_wht': [1, 20, 5, 5, 5, 5], 'dmg_eth_blk': [1, 24, 6, 6, 6, 6], 'dmg_eth_asn': [1, 28, 7, 7, 7, 7]}

        gd2.assign_demographics_for_grouping(group_num, student_info_pool, demographic_totals)
        bcounts = {1: 0, 2: 0, 3: 0, 4: 0}
        acounts = {1: 0, 2: 0, 3: 0, 4: 0}
        wcounts = {1: 0, 2: 0, 3: 0, 4: 0}
        for perf_lvl, stud_list in student_info_pool.items():
            self.assertEqual(len(stud_list), 50)
            for stu in stud_list:
                if stu.dmg_eth_wht is True:
                    wcounts[perf_lvl] += 1
                if stu.dmg_eth_blk is True:
                    bcounts[perf_lvl] += 1
                if stu.dmg_eth_asn is True:
                    acounts[perf_lvl] += 1
        print(bcounts)
        print(acounts)
        print(wcounts)
        self.assertEqual(bcounts[1], 6)
        self.assertEqual(acounts[2], 7)
        self.assertEqual(wcounts[3], 5)
        self.assertEqual(wcounts[4], 5)

    def test_assign_demographic_to_students(self):
        demographic_name = 'dem1'
        perf_lvl_lst = [he.StudentInfo(3, 'female', 12)] * 10
        student_pool = {1: [he.StudentInfo(3, 'male', 12)] * 10,
                        2: perf_lvl_lst[:],
                        3: [he.StudentInfo(3, 'male', 12)] * 10,
                        4: [he.StudentInfo(3, 'female', 12)] * 10}
        count = 10
        performance_level = 2

        gd2.assign_demographic_to_students(demographic_name, student_pool, count, performance_level)
        print(perf_lvl_lst)
        self.assertEqual(len(perf_lvl_lst), 10)
        for stud_info in perf_lvl_lst:
            self.assertTrue(stud_info.dem1)

    def test_assign_demographic_to_students_2(self):
        demographic_name = 'dmg_prg_tt1'
        perf_lvl_lst_1 = [he.StudentInfo(3, 'male', 12) for _i in range(10)]
        perf_lvl_lst_2 = [he.StudentInfo(3, 'female', 12) for _i in range(10)]
        perf_lvl_lst_3 = [he.StudentInfo(3, 'male', 12) for _i in range(10)]
        perf_lvl_lst_4 = [he.StudentInfo(3, 'female', 12) for _i in range(10)]

        student_pool = {1: perf_lvl_lst_1[:],
                        2: perf_lvl_lst_2[:],
                        3: perf_lvl_lst_3[:],
                        4: perf_lvl_lst_4[:]}
        count = 5
        performance_level = 1

        gd2.assign_demographic_to_students(demographic_name, student_pool, count, performance_level)

        num_true = 0
        print(perf_lvl_lst_1)
        self.assertEqual(len(perf_lvl_lst_1), 10)
        for stud_info in perf_lvl_lst_1:
            if stud_info.dmg_prg_tt1 is True:
                num_true += 1

        self.assertEqual(num_true, 5)

    def test_create_student_info_dict(self):
        group_num = 1
        score_pool = {1: [x for x in range(100)], 2: [x for x in range(100)],
                      3: [x for x in range(100)], 4: [x for x in range(100)]}
        demographic_totals = {'male': [1, 20, 5, 5, 5, 5], 'female': [1, 24, 6, 6, 6, 6], 'not specified': [1, 28, 7, 7, 7, 7]}
        grade = 3
        result = gd2.create_student_info_dict(group_num, score_pool, demographic_totals, grade)

        for perf_lvl in result:
            self.assertEqual(len(result[perf_lvl]), 18)

    def test_create_student_infos_by_gender(self):
        gender = 'male'
        count = 30
        performance_level = 1
        score_pool = {1: [x for x in range(count)]}
        grade = 3
        studentInfo_list = gd2.create_student_infos_by_gender(gender, count, performance_level, score_pool, grade)
        self.assertEqual(len(studentInfo_list), count)
        print(studentInfo_list[0].asmt_scores)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
