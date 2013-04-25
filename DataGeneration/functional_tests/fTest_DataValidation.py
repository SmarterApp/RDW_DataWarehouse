import unittest
import csv
import os
import entities
import itertools
from generate_data import ENTITY_TO_PATH_DICT
from zope.component.tests.examples import comp
from dg_types import *


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

GRADES = 'grades'
STUDENTS = 'students'
STATE_TYPE = 'stateType'
#DISTRICT_TYPES_AND_COUNTS = 'districtTypesAndCounts'
typical1 = get_states()[0]['state_type']
DISTRICT_COUNT = sum(get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS].values())
# Get district count for Big, Medium & Small district (config file)
big_school = get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS]['Big']
medium_school = get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS]['Medium']
small_school = get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS]['Small']

# Count Max & Min school numbers for Big, Medium and Small districts
big_min = (get_district_types()['Big'][SCHOOL_COUNTS][MIN]) * (big_school)
big_max = (get_district_types()['Big'][SCHOOL_COUNTS][MAX]) * (big_school)
medium_min = (get_district_types()['Medium'][SCHOOL_COUNTS][MIN]) * (medium_school)
medium_max = (get_district_types()['Medium'][SCHOOL_COUNTS][MAX]) * (medium_school)
small_min = (get_district_types()['Small'][SCHOOL_COUNTS][MIN]) * (small_school)
small_max = get_district_types()['Small'][SCHOOL_COUNTS][MAX] * (small_school)

# Get scores from config file
min_asmt_score = get_scores()[MIN]
max_asmt_score = get_scores()[MAX]
cut_point1 = get_scores()[CUT_POINTS][0]
cut_point2 = get_scores()[CUT_POINTS][1]
cut_point3 = get_scores()[CUT_POINTS][2]


class DataGenerationValidation(unittest.TestCase):
# Get header values from Configuration file
    dim_inst_hier = entities.InstitutionHierarchy.getHeader()
    dim_staff = entities.Staff.getHeader()
    dim_student = entities.Student.getHeader()
    dim_section = entities.Section.getHeader()
    dim_asmt = entities.Assessment.getHeader()
    fact_asmt_outcome = entities.AssessmentOutcome.getHeader()
    external_user_student_rel = entities.ExternalUserStudent.getHeader()

    # Create dictionary to store Headers
    header_dict = {}
    # print(table)
    header_dict['dim_inst_hier'] = dim_inst_hier
    header_dict['dim_staff'] = dim_staff
    header_dict['dim_student'] = dim_student
    header_dict['dim_section'] = dim_section
    header_dict['dim_asmt'] = dim_asmt
    header_dict['fact_asmt_outcome'] = fact_asmt_outcome
    header_dict['external_user_student_rel'] = external_user_student_rel

# Method to read DictReader
    @staticmethod
    def dict_reader(file_path, file_format):
        with open(file_path) as csvFile:
            fileValue = csv.DictReader(csvFile, delimiter=',')
            print('OPEN')
            return fileValue

# Method for comparing headers
    @staticmethod
    def getting_header(path, format_name):
        with open(path, format_name) as csvfile:
            col_reader = csv.reader(csvfile, delimiter=',')
            header_list = (list(col_reader))
            first_row = header_list[0]
            return first_row

    @staticmethod
    def score_fact_asmt(score_column_name, range_min_column_name, range_max_column_name):
            real_score = []
            min_score = []
            max_score = []
            asmt_score_dict = {}
            csv_path = os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv')
            with open(csv_path, 'r') as csvfile:
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    score = values[score_column_name]
                    real_score.append(score)
                    min_score_range = values[range_min_column_name]
                    min_score.append(min_score_range)
                    max_score_range = values[range_max_column_name]
                    max_score.append(max_score_range)
                for i in range(len(real_score)):
                    min_value = int(min_score[i])
                    max_value = int(max_score[i])
                    actual_score = int(real_score[i])
                    assert min_asmt_score <= actual_score and min_value and max_value <= max_asmt_score, ('Incorrect score: Actual score: ' + str(actual_score) + ' Min_Score: ' + str(min_value) + ' Max_Score: ' + str(max_value))
                    if min_value != min_asmt_score and max_value != max_asmt_score:
                        assert (actual_score - min_value) == (max_value - actual_score), ('Min/Max scores are not in range in fact_asmt_outcome file. Actual score: ' + str(actual_score) + ' Min_Score: ' + str(min_value) + ' Max_Score: ' + str(max_value))

    # TC1: Check Headers in all the CSV files
    def test_headers(self):
        csv_path = ENTITY_TO_PATH_DICT.values()
        for each_csv in csv_path:
        # do validate
            actual_headers = DataGenerationValidation.getting_header(each_csv, 'r')
            expected_headers = DataGenerationValidation.header_dict.get(os.path.basename(each_csv)[:-4])
            assert expected_headers is not None, ('No header info for %s' % each_csv)
            assert len(actual_headers) == len(expected_headers), ('Number of header does not match: %s' % each_csv)
            for header in expected_headers:
                assert header in actual_headers, ('Header Name: %s is missing in %s file' % (header, os.path.basename(each_csv)[:-4]))
        print('TC1: Passed: Check Headers in all the CSV files')

    # TC2: Validate min/Max assessment score, cut score and assessment performance level name
    def test_asmt_cut_lavel_score(self):
        csv_path = os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_asmt.csv')
        with open(csv_path, 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            for values in col_val:
                asmt_score_min = values['asmt_score_min']
                asmt_score_max = values['asmt_score_max']
                asmt_cut_point_1 = values['asmt_cut_point_1']
                asmt_cut_point_2 = values['asmt_cut_point_2']
                asmt_cut_point_3 = values['asmt_cut_point_3']
                asmt_cut_point_4 = values['asmt_cut_point_4']
                asmt_perf_lvl_name_1 = values['asmt_perf_lvl_name_1']
                asmt_perf_lvl_name_2 = values['asmt_perf_lvl_name_2']
                asmt_perf_lvl_name_3 = values['asmt_perf_lvl_name_3']
                asmt_perf_lvl_name_4 = values['asmt_perf_lvl_name_4']
            asmt_dict = {'asmt_score_min': [int(asmt_score_min), min_asmt_score],
                         'asmt_score_max': [int(asmt_score_max), max_asmt_score],
                         'asmt_cut_point_1': [int(asmt_cut_point_1), cut_point1],
                         'asmt_cut_point_2': [int(asmt_cut_point_2), cut_point2],
                         'asmt_cut_point_3': [int(asmt_cut_point_3), cut_point3],
                         'asmt_cut_point_4': [(asmt_cut_point_4), ''],
                         'asmt_perf_lvl_name_1': [(asmt_perf_lvl_name_1), 'Minimal Understanding'],
                         'asmt_perf_lvl_name_2': [(asmt_perf_lvl_name_2), 'Partial Understanding'],
                         'asmt_perf_lvl_name_3': [(asmt_perf_lvl_name_3), 'Adequate Understanding'],
                         'asmt_perf_lvl_name_4': [(asmt_perf_lvl_name_4), 'Thorough Understanding']}
            for key, value in asmt_dict.items():
                    csv_asmt_value = value[0]
                    config_asmt_value = value[1]
                    assert csv_asmt_value == config_asmt_value, (key + ' value is incorrect. Expected ' + str(config_asmt_value) + ' but found ' + str(csv_asmt_value))
        print('TC2: Passed: Validate min/Max assessment score, cut score and assessment performance level names')

    # TC3: Validate School Categoty
    # dim_inst_hier--> school category/ school_guid
    def test_grade(self):
        expected_school_category = ['High School', 'Middle School', 'Elementary School']
        csv_path = os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_inst_hier.csv')
        with open(csv_path, 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            dict = {}
            actual_school_category = []
            for school in col_val:
                all_school = school['school_category']
                # check the value is available in the List ot not if not add value in the list so we can compare with expected_school_categoty
                if all_school in actual_school_category:
                    pass
                else:
                    actual_school_category.append(all_school)
                school_id = school['school_guid']
                # Get all the IDs for each school_categoty (High, Middle & Elementery) - without repeating school category
                if dict.get(all_school):
                    dict[all_school].append(school_id)
                else:
                    dict[all_school] = [school_id]
            # Comparing school category
            assert sorted(expected_school_category) == sorted(actual_school_category), 'School Category does not match'
        # get school_guid from dim_section and check the grades
        csv_files = [os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_section.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_student.csv')]
        for each_file in csv_files:
            with open(each_file, 'r') as csvfile:
                grade_dict = {}
                sec_dic = {}
                expexted_grade = ['3', '4', '5', '6', '7', '8', '11']
                actual_grade = []
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    if os.path.basename(each_file)[:-4] == 'dim_section'or os.path.basename(each_file)[:-4] == 'dim_student':
                        section_grade = values['grade']
                        school_guid = values['school_guid']
                    else:
                        section_grade = values['asmt_grade']
                        school_guid = values['school_guid']
                    if section_grade in grade_dict:
                        if school_guid not in grade_dict[section_grade]:
                            grade_dict[section_grade].append(school_guid)
                    else:
                        grade_dict[section_grade] = [school_guid]
                    if section_grade not in actual_grade:
                        actual_grade.append(section_grade)
                assert sorted(expexted_grade) == sorted(actual_grade), ('Expected Grades:', sorted(expexted_grade), 'but found:', sorted(actual_grade), 'in', os.path.basename(each_file)[:-4])

            # High school - Grades from dim_section
                uniq_hi_list = []
                overall_highschool_list = grade_dict['11']
                for values in overall_highschool_list:
                    if values not in uniq_hi_list:
                        uniq_hi_list.append(values)
                # High school - School category from dim_inst_hier
                overall_highschool = dict['High School']
                # Validate Grades according to the school category
                assert uniq_hi_list == overall_highschool, 'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4]
            # Middle School
            uniq_ml_list = []
            overall_middleschool_list = grade_dict['6'] + grade_dict['7'] + grade_dict['8']
            for values in overall_middleschool_list:
                if values not in uniq_ml_list:
                    uniq_ml_list.append(values)

            overall_middleschool = dict['Middle School']
            assert uniq_ml_list == overall_middleschool, 'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4]

            # Elementary School
            uniq_el_list = []
            overall_elementaryschool_list = grade_dict['3'] + grade_dict['4'] + grade_dict['5']
            for values in overall_elementaryschool_list:
                if values not in uniq_el_list:
                    uniq_el_list.append(values)
            overall_elementaryschool = dict['Elementary School']
            assert uniq_el_list == overall_elementaryschool, 'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4]
        print('TC3: Passed: Validate School Categoty and grades respect to School Category')

    # TC4: Check Ids are not empty in all CSVs
    def test_primary_key(self):
        # class_names = ENTITY_TO_PATH_DICT
        all_files = ENTITY_TO_PATH_DICT.values()
        for csv_file in all_files:
            with open(csv_file, 'r') as csvfile6:
                col_val = csv.reader(csvfile6, delimiter=',')
                header = next(col_val)
                #print('header: ', header)
                for row in col_val:
                    assert row[0] != '', ('Primary id is empty in: ', os.path.basename(csv_file)[:-4])
        print('TC4: Passed: Validate Primary Keys are not empty in all CSVs')

    # TC5: Validate scores in fact_asmt_outcome file
    def test_fact_score(self):
            all_score_outcome = [['asmt_score', 'asmt_score_range_min', 'asmt_score_range_max'],
                                 ['asmt_claim_1_score', 'asmt_claim_1_score_range_min', 'asmt_claim_1_score_range_max'],
                                 ['asmt_claim_2_score', 'asmt_claim_2_score_range_min', 'asmt_claim_2_score_range_max'],
                                 ['asmt_claim_3_score', 'asmt_claim_3_score_range_min', 'asmt_claim_3_score_range_max']]
            for score_part in all_score_outcome:
                DataGenerationValidation.score_fact_asmt(score_part[0], score_part[1], score_part[2])
            print('TC5: Passed: Validate scores in fact_asmt_outcome file')

    # TC6: check assessment performance level in fact_asmt_outcome
    def test_performence_level(self):
        perf_lvl = []
        asmt_score_list = []
        csv_path = os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv')
        with open(csv_path, 'r') as csvfile:
                    col_val = csv.DictReader(csvfile, delimiter=',')
                    for values in col_val:
                        asmt_perf_lvl = values['asmt_perf_lvl']
                        perf_lvl.append(asmt_perf_lvl)
                        asmt_score = values['asmt_score']
                        asmt_score_list.append(asmt_score)
                    for i in range(len(asmt_score_list)):
                        if min_asmt_score <= (int(asmt_score_list[i])) <= (cut_point1 - 1) and (int(perf_lvl[i])) == 1:
                            pass
                        elif cut_point1 <= (int(asmt_score_list[i])) <= (cut_point2 - 1) and (int(perf_lvl[i])) == 2:
                            pass
                        elif cut_point2 <= (int(asmt_score_list[i])) <= (cut_point3 - 1) and (int(perf_lvl[i])) == 3:
                            pass
                        elif cut_point3 <= (int(asmt_score_list[i])) <= max_asmt_score and (int(perf_lvl[i])) == 4:
                            pass
                        else:
                            raise AssertionError('Fail: fact_asmt_outcome file. Asseessment score:' + asmt_score_list[i] + ' and Performance_level:' + perf_lvl[i])
        print('TC6: Passed: Validate Performance level in fact_asmt_outcome file')

    # TC7: Count number of discticts from CSVs and compare with Config file
    def test_number_of_districts(self):
        csv_files = [os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_inst_hier.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_section.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_staff.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_student.csv')]
        for each_csv in csv_files:
            district_list = []
            with open(each_csv, 'r') as csvfile:
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    district_guid = values['district_guid']
                    if district_guid != 'NA':
                        district_list.append(district_guid)

            district_list = list(set(district_list))
            assert DISTRICT_COUNT == len(district_list), 'District count in config file is ' + str(DISTRICT_COUNT) + ' but District count in ' + os.path.basename(each_csv)[:-4] + ' is ' + str(len(district_list))
        print('TC7: Passed: Count overall number of discticts from CSVs and compare with Config file')

    # TC8: Count number of schools from CSVs and compare with Config file
    def test_number_of_schools(self):
        # Minimum schools in Big, Medium and Small districts
        min_schools = big_min + medium_min + small_min
        # Maximum schools in Big, Medium and Small districts
        max_schools = big_max + medium_max + small_max
        csv_files = [os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_inst_hier.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_section.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_staff.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_student.csv')]
        for each_csv in csv_files:
            school_list = []
            with open(each_csv, 'r') as csvfile:
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    school_guid = values['school_guid']
                    if school_guid != 'NA':
                        school_list.append(school_guid)
            school_list = list(set(school_list))
            assert min_schools <= len(school_list) <= max_schools, 'Min School count in config file is ' + str(min_schools) + ' Max School count in config file is ' + str(max_schools) + ' but School count in ' + os.path.basename(each_csv)[:-4] + ' is ' + str(len(school_list))
        print('Passed: TC8: Count overall number of schools from CSVs and compare with Config file ')

    # TC9: Count number of students from CSVs and compare with Config file
    def test_number_of_students(self):
        size_types = get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS].keys()
        for each_type in size_types:
            min_type = get_district_types()[each_type][SCHOOL_COUNTS][MIN]
            max_type = get_district_types()[each_type][SCHOOL_COUNTS][MAX]
            school_types = get_school_types().keys()
            min_list = []
            max_list = []
            for each_school_types in school_types:
                garde_len = len(get_school_types()[each_school_types][GRADES])
                student_min = get_school_types()[each_school_types][STUDENTS][MIN]
                student_max = get_school_types()[each_school_types][STUDENTS][MAX]
                assert (0 <= student_min <= student_max)
                min_list.append(student_min * garde_len)
                max_list.append(student_max * garde_len)
        # Get overall Min & Max Students
        min_overall_students = ((big_min) + (medium_min) + (small_min)) * (min(min_list))  # big_min/medium_min/small_min
        max_overall_students = ((big_max) + (medium_max) + (small_max)) * (max(max_list))  # big_max/medium_max/small_max
        csv_files = [os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                     os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_student.csv')]
        for each_csv in csv_files:
            student_list = []
            with open(each_csv, 'r') as csvfile:
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    student_guid = values['student_guid']
                    student_list.append(student_guid)
            student_list = list(set(student_list))
            assert min_overall_students <= len(student_list) <= max_overall_students, 'Min Student count in config file is ' + str(min_overall_students) + ' Max Student count in config file is ' + str(max_overall_students) + ' but Student count in ' + os.path.basename(each_csv)[:-4] + ' is ' + str(len(student_list))
        print('Passed: TC9: Count overall number of students from CSVs and compare with Config file ')

    # TC10: Count Subjects & percentages
    def test_subjects_and_percentage(self):
        # Values from config file
        #typical1 = get_states()[0]['state_type']
        math_percentage = get_state_types()[typical1]['subjects_and_percentages']['Math']
        ela_percentage = get_state_types()[typical1]['subjects_and_percentages']['ELA']
        both_count = 0
        math_only_count = 0
        ela_only_count = 0
        student_id_dict = {}
        math_guid = []
        ela_guid = []

        with open(os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_section.csv'), 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            for values in col_val:
                section_guid = values['section_guid']
                subject_name = values['subject_name'].lower()
                if subject_name == 'math':
                    math_guid.append(section_guid)
                elif subject_name == 'ela':
                    ela_guid.append(section_guid)
                else:
                    print('Subject names are incorrrect in dim_section file')
        with open(os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv'), 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            for values in col_val:
                student_guid = values['student_guid']
                section_guid = values['section_guid']
                if student_guid in student_id_dict:
                        student_id_dict[student_guid].append(section_guid)
                else:
                    student_id_dict[student_guid] = [section_guid]
        for key, value in student_id_dict.items():
            if len(value) == 2:
                if (value[0] in math_guid and value[1] in ela_guid) or (value[1] in math_guid and value[0] in ela_guid):
                    both_count += 1
                else:
                    print('Math & ELA: Section ID in fact_asmt_outcome file do not match with section ID in dim_section file')
            elif len(value) == 1:
                if (value[0] in math_guid):
                    math_only_count += 1
                elif (value[0] in ela_guid):
                    ela_only_count += 1
                else:
                    print('Math OR ELA: Section ID in fact_asmt_outcome file do not match with section ID in dim_section file')
            else:
                print('Error: One student has more then two sections(Math & ELA)')
        total_student_count = len(student_id_dict.keys())
        both_perc = round((1.0 * both_count / total_student_count), 1)
        math_perc = round((1.0 * (both_count + math_only_count) / total_student_count), 1)
        ela_perc = round((1.0 * (both_count + ela_only_count) / total_student_count), 1)
        assert math_percentage == math_perc, 'Math subject and percentage does not match. Expected ' + str(math_percentage) + ' but found ' + str(math_perc)
        assert ela_percentage == ela_perc, 'ELA subject and percentage does not match. Expected ' + str(ela_percentage) + ' but found ' + str(ela_perc)
        print('Passed: TC10: Count Subjects & percentages ')
