# '''
# Created on Apr 17, 2013
#
# @author: swimberly
# '''
# import unittest
# import os
# from datetime import date
# import DataGeneration.src.generate_data as generate_data
# import DataGeneration.src.generate_entities as generate_entities
# from DataGeneration.src.helper_entities import District
# from DataGeneration.src.entities import Staff, AssessmentOutcome, InstitutionHierarchy
#
#
# class Test(unittest.TestCase):
#
#     def setUp(self):
#         self.cut_points = [1400, 1800, 2100]
#         self.perf_lvl_dist = {'ELA': {'3': {'percentages': [30, 34, 28, 9]}},
#                               'Math': {'3': {'percentages': [14, 42, 37, 7]}}}
#         self.score_details = {'min': 1200, 'max': 2400, 'cut_points': [1400, 1800, 2100]}
#         self.config_module = DummyClass()
#         self.config_module.PERCENTAGES = 'percentages'
#         self.config_module.MIN = 'min'
#         self.config_module.MAX = 'max'
#         self.config_module.AVG = 'avg'
#         self.config_module.CUT_POINTS = 'cut_points'
#         self.config_module.FROM_DATE = 'from_date'
#         self.config_module.MOST_RECENT = 'most_recent'
#         self.config_module.TO_DATE = 'to_date'
#         self.config_module.GRADES = 'grades'
#         self.config_module.TYPE = 'type'
#         self.config_module.get_temporal_information = self.get_temporal_information_mock
#         generate_data.config_module = self.config_module
#
#     def test_generate_name_list_dictionary(self):
#         list_name_to_path_dictionary = {}
#         file_count = 10
#         name_count = 50
#         file_names = self.create_mock_name_files(file_count, name_count)
#         for name in file_names:
#             list_name_to_path_dictionary[name] = name
#         res = generate_data.generate_name_list_dictionary(list_name_to_path_dictionary)
#
#         self.assertEqual(len(res), file_count)
#         for name in res:
#             number_of_lines = len(res[name])
#             self.assertEqual(number_of_lines, name_count)
#         self.remove_files(file_names)
#
#     def test_generate_district_dictionary(self):
#         district_types = {'Big': 2, 'Medium': 6, 'Small': 40}
#         res = generate_data.generate_district_dictionary(district_types, ['n1', 'n2', 'n3', 'n4'], ['n11', 'n22', 'n33', 'n44'])
#         self.assertEqual(len(res['Big']), 2)
#         self.assertEqual(len(res['Medium']), 6)
#         self.assertEqual(len(res['Small']), 40)
#
#         for item in res['Big']:
#             self.assertIsInstance(item, District)
#             self.assertIsNotNone(item.district_name)
#             self.assertIsNotNone(item.district_guid)
#         for item in res['Medium']:
#             self.assertIsInstance(item, District)
#             self.assertIsNotNone(item.district_name)
#             self.assertIsNotNone(item.district_guid)
#         for item in res['Small']:
#             self.assertIsInstance(item, District)
#             self.assertIsNotNone(item.district_name)
#             self.assertIsNotNone(item.district_guid)
#
#     def test_create_school_dictionary(self):
#         school_counts = {'min': 100, 'max': 310, 'avg': 500}
#         ratios = {'High School': 1, 'Middle School': 2, 'Elementary School': 5}
#         school_types_dict = {'High School': {'type': 'High School', 'grades': [11], 'students': {'min': 50, 'max': 250, 'avg': 100}},
#                              'Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 25, 'max': 100, 'avg': 50}},
#                              'Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 10, 'max': 35, 'avg': 30}}}
#         name_list1 = ['name_%d' % i for i in range(20)]
#         name_list2 = ['name2_%d' % i for i in range(20)]
#         res = generate_data.create_school_dictionary(self.config_module, school_counts, ratios, school_types_dict, name_list1, name_list2)
#         self.assertEqual(len(res), 3)
#         elm_sch_len = len(res['Elementary School'])
#         mid_sch_len = len(res['Middle School'])
#         hig_sch_len = len(res['High School'])
#         school_sum = elm_sch_len + mid_sch_len + hig_sch_len
#         self.assertGreaterEqual(school_sum, school_counts['min'])
#         self.assertLessEqual(school_sum, school_counts['max'])
#
#     def test_generate_institution_hierarchy_from_helper_entities(self):
#         state = DummyClass()
#         state.state_name = 'Georgia'
#         state.state_code = 'GA'
#         district = DummyClass()
#         district.district_guid = 'dguid1'
#         district.district_name = 'District1'
#         school = DummyClass()
#         school.school_name = 'School1'
#         school.school_guid = 'sguid1'
#         school.school_category = 'Middle'
#
#         res = generate_data.generate_institution_hierarchy_from_helper_entities(self.config_module, state, district, school)
#
#         self.assertIsInstance(res, InstitutionHierarchy)
#         self.assertEqual(res.state_name, 'Georgia')
#         self.assertEqual(res.state_code, 'GA')
#         self.assertEqual(res.district_name, 'District1')
#         self.assertEqual(res.school_name, 'School1')
#         self.assertEqual(res.school_category, 'Middle')
#
#     def test_generate_list_of_scores(self):
#         total = 100
#         percentages = self.perf_lvl_dist['ELA']['3']['percentages']
#         res = generate_data.generate_list_of_scores(self.config_module, total, self.score_details, percentages, 'Math', 3)
#         self.assertEqual(len(res), 100)
#         for score in res:
#             self.assertGreaterEqual(score, self.score_details['min'])
#             self.assertLessEqual(score, self.score_details['max'])
#
#     def test_generate_assessment_outcomes_from_helper_entities_and_lists(self):
#         grade = 5
#         district_guid = 'dist123'
#         school_guid = 'scho2343'
#         school_name = 'school1'
#         state_code = 'GA'
#         section_guid = 'sect123'
#         subject = 'Math'
#         students = self.create_students(10, grade, subject, section_guid, school_guid, state_code, district_guid)
#         scores = [1300, 1400, 1500, 1700, 1800, 1900, 2000, 2100, 2200, 2300]
#         teacher_guid = 'teach234'
#         section = DummyClass()
#         section.grade = grade
#         section.section_guid = section_guid
#         section.section_rec_id = 12343
#         institution_hierarchy = DummyClass()
#         institution_hierarchy.inst_hier_rec_id = 23
#         institution_hierarchy.state_code = state_code
#         institution_hierarchy.district_guid = district_guid
#         institution_hierarchy.school_guid = school_guid
#         institution_hierarchy.school_name = school_name
#         assessment = self.create_assessment(grade, subject)
#         ebmin = 32
#         ebmax = 8
#         rndlo = -10
#         rndhi = 25
#         batch_guid = '00000000-0000-0000-0000-000000000000'
#
#         res = generate_data.generate_assessment_outcomes_from_helper_entities_and_lists(students, scores, teacher_guid, section, institution_hierarchy,
#                                                                                         assessment, ebmin, ebmax, rndlo, rndhi, batch_guid)
#
#         expected_scores = scores[:]
#         self.assertEqual(len(res), 10)
#         for i in range(len(res)):
#             self.assertIsInstance(res[i], AssessmentOutcome)
#             self.assertIn(res[i].asmt_score, expected_scores)
#             expected_scores.remove(res[i].asmt_score)
#
#     def test_translate_scores_to_assessment_score(self):
#         assmt = self.create_assessment(5, 'Math')
#         scores = [2180, 1200, 2400, 1590, 1890, 1800, 2100, 1400]
#         expected_pl = [4, 1, 4, 2, 3, 3, 4, 2]
#         res = generate_data.translate_scores_to_assessment_score(scores, self.cut_points, assmt, 32, 8, -10, 25)
#         for i in range(len(res)):
#             self.assertEqual(res[i].perf_lvl, expected_pl[i])
#             self.assertIn(res[i].perf_lvl, [1, 2, 3, 4])
#
#     def test_generate_students_from_institution_hierarchy(self):
#         number_of_students = 50
#         institution_hierarchy = DummyClass()
#         institution_hierarchy.state_code = 'GA'
#         institution_hierarchy.district_guid = 'dist123'
#         institution_hierarchy.school_guid = 'scho2343'
#         institution_hierarchy.school_name = 'school1'
#         grade = 10
#         section_guid = 'sect123'
#         street_names = ['Broadway', 'Wall', 'Spring', 'Houston', 'Washington', 'Main', 'Fulton', 'Chambers']
#
#         res = generate_data.generate_students_from_institution_hierarchy(self.config_module, number_of_students, institution_hierarchy, grade, section_guid, street_names)
#         self.assertEqual(len(res), number_of_students)
#         for student in res:
#             street_name = student.address_1.split()[1]
#             self.assertIn(street_name, street_names)
#             self.assertEqual(institution_hierarchy.state_code, student.state_code)
#             self.assertEqual(institution_hierarchy.district_guid, student.district_guid)
#             self.assertEqual(institution_hierarchy.school_guid, student.school_guid)
#             self.assertEqual(student.grade, grade)
#
#     def test_set_students_rec_id_and_section_id(self):
#         old_section_guid = 'old_id'
#         students = generate_entities.generate_students(10, old_section_guid, 5, 'SC', '123', '234', 'school', ['a', 'b'], date.today(), True)
#         for stu in students:
#             self.assertEqual(stu.section_guid, old_section_guid)
#         students = generate_data.set_students_rec_id_and_section_id(students, 'new_id')
#         for stu in students:
#             self.assertEqual(stu.section_guid, 'new_id')
#
#         students = generate_entities.generate_students(10, old_section_guid, 5, 'SC', '123', '234', 'school', ['a', 'b'], date.today(), True)
#         for stu in students:
#             self.assertEqual(stu.section_guid, old_section_guid)
#         generate_data.set_students_rec_id_and_section_id(students, 'new_id')
#         for stu in students:
#             self.assertEqual(stu.section_guid, 'new_id')
#
#     def test_generate_teaching_staff_from_institution_hierarchy(self):
#         num_of_staff = 20
#         institution_hierarchy = DummyClass()
#         institution_hierarchy.state_code = 'GA'
#         institution_hierarchy.district_guid = 'dict1234'
#         institution_hierarchy.school_guid = 'sch1234'
#         section_guid = 'sect234'
#         temp_data = self.get_temporal_information_mock()
#
#         res = generate_data.generate_teaching_staff_from_institution_hierarchy(self.config_module, num_of_staff, institution_hierarchy, section_guid)
#
#         self.assertEqual(len(res), num_of_staff)
#         for staff in res:
#             self.assertIsInstance(staff, Staff)
#             self.assertEqual(staff.hier_user_type, 'Teacher')
#             self.assertEqual(staff.to_date, temp_data['to_date'])
#             self.assertEqual(staff.from_date, temp_data['from_date'])
#             self.assertEqual(staff.most_recent, temp_data['most_recent'])
#             self.assertEqual(staff.state_code, 'GA')
#             self.assertEqual(staff.district_guid, 'dict1234')
#             self.assertEqual(staff.school_guid, 'sch1234')
#             self.assertEqual(staff.section_guid, 'sect234')
#
#     def test_generate_non_teaching_staff(self):
#         state_code = 'GA'
#         num_of_staff = 20
#         temp_data = self.get_temporal_information_mock()
#         district_guid = 'distguid'
#         school_guid = 'schoolguid'
#         res = generate_data.generate_non_teaching_staff(self.config_module, num_of_staff, state_code, district_guid, school_guid)
#         self.assertEqual(len(res), num_of_staff)
#         for staff in res:
#             self.assertIsInstance(staff, Staff)
#             self.assertEqual(staff.hier_user_type, 'Staff')
#             self.assertEqual(staff.to_date, temp_data['to_date'])
#             self.assertEqual(staff.from_date, temp_data['from_date'])
#             self.assertEqual(staff.most_recent, temp_data['most_recent'])
#             self.assertEqual(staff.state_code, state_code)
#             self.assertEqual(staff.district_guid, district_guid)
#             self.assertEqual(staff.school_guid, school_guid)
#
#     def test_calculate_number_of_schools(self):
#         res = generate_data.calculate_number_of_schools(100, 800, 200)
#         self.assertIsInstance(res, int)
#
#     def test_calculate_number_of_students(self):
#         res = generate_data.calculate_number_of_students(100, 800, 200)
#         self.assertIsInstance(res, int)
#
#     def test_calculate_number_of_sections(self):
#         # TODO: write more test when the method is implemented
#         res = generate_data.calculate_number_of_sections(15)
#         self.assertIsInstance(res, int)
#
#     def test_calcuate_claim_scores(self):
#         assmt = self.create_assessment(1, 'ELA')
#         res = generate_data.calculate_claim_scores(2105, assmt, 32, 8, -10, 25)
#         expected_claims = 3
#         self.assertEqual(len(res), expected_claims)
#         for claim in res:
#             self.assertGreaterEqual(claim.claim_score, assmt.asmt_claim_1_score_min)
#             self.assertLessEqual(claim.claim_score, assmt.asmt_claim_1_score_max)
#             self.assertGreaterEqual(claim.claim_score_interval_minimum, assmt.asmt_claim_1_score_min)
#             self.assertLessEqual(claim.claim_score_interval_maximum, assmt.asmt_claim_1_score_max)
#             self.assertGreaterEqual(claim.claim_score_interval_maximum, claim.claim_score)
#             self.assertLessEqual(claim.claim_score_interval_minimum, claim.claim_score)
#
#     def test_get_flat_grades_list(self):
#         school_config = {
#             'High School': {'grades': [11], 'students': {'min': 100, 'max': 500, 'avg': 300}},
#             'Jr. High School': {'grades': [9, 10, 11], 'students': {'min': 100, 'max': 500, 'avg': 300}},
#             'Middle School': {'grades': [6, 7, 8], 'students': {'min': 50, 'max': 200, 'avg': 150}},
#             'Elementary School': {'grades': [1, 3, 4, 5], 'students': {'min': 20, 'max': 70, 'avg': 60}}
#         }
#         expected_items = [11, 9, 10, 6, 7, 8, 1, 3, 4, 5]
#         res = generate_data.get_flat_grades_list(school_config, 'grades')
#         self.assertEqual(len(res), len(expected_items))
#         for it in expected_items:
#             self.assertIn(it, res)
#         diffs = set(expected_items) ^ set(res)
#         self.assertFalse(diffs)
#
#     def test_select_assessment_from_list(self):
#         asmt_list = [self.create_assessment(1, 'Math'), self.create_assessment(2, 'Math'), self.create_assessment(3, 'Math'),
#                      self.create_assessment(1, 'ELA'), self.create_assessment(2, 'ELA'), self.create_assessment(3, 'ELA'),
#                      self.create_assessment(6, 'Math'), self.create_assessment(8, 'ELA'), self.create_assessment(12, 'Math')]
#         assessment = generate_data.select_assessment_from_list(asmt_list, 1, 'Math')
#         self.assertEqual(assessment.asmt_grade, 1)
#         self.assertEqual(assessment.asmt_subject, 'Math')
#
#         assessment = generate_data.select_assessment_from_list(asmt_list, 6, 'Math')
#         self.assertEqual(assessment.asmt_grade, 6)
#         self.assertEqual(assessment.asmt_subject, 'Math')
#
#         assessment = generate_data.select_assessment_from_list(asmt_list, 10, 'ELA')
#         self.assertIsNone(assessment)
#
#         assessment = generate_data.select_assessment_from_list([], 10, 'ELA')
#         self.assertIsNone(assessment)
#
#     def test_get_subset_of_students(self):
#         students = [object()] * 100
#         res = generate_data.get_subset_of_students(students, .9)
#         self.assertEqual(len(res), 90)
#
#     # ----------------------
#     # Helper functions
#     # ----------------------
#     def create_assessment(self, grade, subject):
#         assmt = DummyClass()
#         assmt.asmt_rec_id = 'asmt_rec_id'
#         assmt.asmt_subject = subject
#         assmt.asmt_grade = grade
#         assmt.asmt_claim_1_name = 'claim1'
#         assmt.asmt_claim_1_score_min = self.score_details['min']
#         assmt.asmt_claim_1_score_max = self.score_details['max']
#         assmt.asmt_claim_1_score_weight = .15 if subject == 'Math' else .4
#         assmt.asmt_claim_2_name = 'claim2'
#         assmt.asmt_claim_2_score_min = self.score_details['min']
#         assmt.asmt_claim_2_score_max = self.score_details['max']
#         assmt.asmt_claim_2_score_weight = .1 if subject == 'Math' else .35
#         assmt.asmt_claim_3_name = 'claim3'
#         assmt.asmt_claim_3_score_min = self.score_details['min']
#         assmt.asmt_claim_3_score_max = self.score_details['max']
#         assmt.asmt_claim_3_score_weight = .3 if subject == 'Math' else .25
#         assmt.asmt_claim_4_name = 'claim4' if subject == 'Math' else None
#         assmt.asmt_claim_4_score_min = self.score_details['min'] if subject == 'Math' else None
#         assmt.asmt_claim_4_score_max = self.score_details['max'] if subject == 'Math' else None
#         assmt.asmt_claim_4_score_weight = .45 if subject == 'Math' else None
#         assmt.asmt_score_min = self.score_details['min']
#         assmt.asmt_score_max = self.score_details['max']
#         assmt.asmt_subject = 'Math'
#         assmt.asmt_cut_point_1 = self.cut_points[0]
#         assmt.asmt_cut_point_2 = self.cut_points[1]
#         assmt.asmt_cut_point_3 = self.cut_points[2]
#         assmt.asmt_cut_point_4 = None
#         assmt.asmt_period_year = 2012
#         assmt.asmt_period = 'Fall'
#
#         # asmts = generate_entities.generate_assessments([5], self.cut_points, date.today(), True, date.today())
#         return assmt  # asmts[0]
#
#     def create_students(self, num, grade, section_guid, school_guid, state_code, subject, district_guid):
#         students = []
#         for i in range(num):
#             student = DummyClass()
#             student.student_guid = section_guid
#             student.student_rec_id = 'rec_%d' % i
#             student.first_name = 'first_%d' % i
#             student.last_name = 'last_%d' % i
#             student.address_1 = '%d Main St.' % i
#             student.city = 'North Carolina'
#             student.zip_code = 12345
#             student.gender = 'Male'
#             student.email = 'email_%d' % i
#             student.dob = date.today()
#             student.grade = grade
#             student.state_code = state_code
#             student.from_date = date.today()
#             student.most_recent = True
#             student.district_guid = district_guid
#             student.school_guid = school_guid
#             students.append(student)
#         return students
#
#     def create_mock_name_files(self, file_count, name_count):
#         list_name = 'unit_test_file_for_testing{num}'
#         file_list = []
#         for i in range(file_count):
#             file_name = list_name.format(num=i)
#             with open(file_name, 'w') as f:
#                 for i in range(name_count):
#                     f.write('name_{0}\n'.format(i))
#             file_list.append(file_name)
#         return file_list
#
#     def remove_files(self, file_list):
#         for name in file_list:
#             os.remove(name)
#
#     def get_temporal_information_mock(self):
#         return {'from_date': '20120901', 'to_date': None, 'most_recent': True, 'date_taken_year': '2012', 'date_taken_month': ''}
#
#
# class DummyClass(object):
#     pass
#
#
# if __name__ == "__main__":
#     # import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()
