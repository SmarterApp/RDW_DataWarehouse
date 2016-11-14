import DataGeneration.src.models.entities as entities
import csv
import os
import unittest
from DataGeneration.src.configs.dg_types_test import get_scores, get_states, get_state_types, get_district_types, get_school_types
from DataGeneration.src.constants.constants import DISTRICT_TYPES_AND_COUNTS, MIN, MAX, CUT_POINTS, SCHOOL_TYPES_AND_RATIOS, SCHOOL_COUNTS, GRADES, STUDENTS


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

typical1 = get_states()[0]['state_type']
DISTRICT_COUNT = sum(get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS].values())

components = __location__.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])
ENTITY_TO_PATH_DICT = {'InstitutionHierarchy': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_inst_hier.csv'),
                       'Section': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_section.csv'),
                       'Assessment': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_asmt.csv'),
                       'AssessmentOutcome': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                       'ExternalUserStudent': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'external_user_student_rel.csv'),
                       'Student': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_student.csv')}

# Get scores from config file
min_asmt_score = get_scores()[MIN]
max_asmt_score = get_scores()[MAX]
cut_point1 = get_scores()[CUT_POINTS][0]
cut_point2 = get_scores()[CUT_POINTS][1]
cut_point3 = get_scores()[CUT_POINTS][2]


@unittest.skip("skipping this test till starschema change has been made")
class DataGenerationValidation(unittest.TestCase):
# Store CSV path in respective variables for each csv
    dim_asmt_csv = os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_asmt.csv')
    dim_inst_hier_csv = os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_inst_hier.csv')
    dim_student_csv = os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_student.csv')
    dim_section_csv = os.path.join(__location__, '..', 'datafiles', 'csv', 'dim_section.csv')
    fact_asmt_outcome_csv = os.path.join(__location__, '..', 'datafiles', 'csv', 'fact_asmt_outcome.csv')

# Get header values from Entities file
    dim_inst_hier = entities.InstitutionHierarchy.getHeader()
    dim_student = entities.Student.getHeader()
    dim_section = entities.Section.getHeader()
    dim_asmt = entities.Assessment.getHeader()
    fact_asmt_outcome = entities.AssessmentOutcome.getHeader()
    external_user_student_rel = entities.ExternalUserStudent.getHeader()

    # Create dictionary to store Headers
    header_dict = {}
    header_dict['dim_inst_hier'] = dim_inst_hier
    header_dict['dim_student'] = dim_student
    header_dict['dim_section'] = dim_section
    header_dict['dim_asmt'] = dim_asmt
    header_dict['fact_asmt_outcome'] = fact_asmt_outcome
    header_dict['external_user_student_rel'] = external_user_student_rel

# Method to read DictReader(Not used)
#    @staticmethod
#    def dict_reader(file_path, file_format):
#        with open(file_path, file_format) as csvFile:
#            fileValue = csv.DictReader(csvFile, delimiter=',')
#            print('OPEN')
#            return fileValue

# Method for comparing headers
    @staticmethod
    def getting_header(path, format_name):
        with open(path, format_name) as csvfile:
            col_reader = csv.reader(csvfile, delimiter=',')
            first_row = next(col_reader)
#            header_list = (list(col_reader))
#            first_row = header_list[0]
            return first_row

    @staticmethod
    def score_fact_asmt(score_column_name, range_min_column_name, range_max_column_name):
            real_score = []
            min_score = []
            max_score = []
            asmt_score_dict = {}
            with open(DataGenerationValidation.fact_asmt_outcome_csv, 'r') as csvfile:
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
                    # Validate that the actual score and actual minimum score is greater than or equal to min range
                    assert min_asmt_score <= actual_score and min_value, ('Incorrect score: Actual score: ' + str(actual_score) + ' Min_Score: ' + str(min_value))
                    # Validate that the actual score and actual maximum score is less than or equal to max range
                    assert max_asmt_score >= actual_score and max_value, ('Incorrect score: Actual score: ' + str(actual_score) + ' Max_Score: ' + str(max_value))
                    # TODO: This is applicable when Edge cases are not symmetrical. Need to update this when the requirement is clarified
                    if min_value != min_asmt_score and max_value != max_asmt_score:
                        assert (actual_score - min_value) == (max_value - actual_score), ('Min/Max scores are not in range in fact_asmt_outcome file. Actual score: ' + str(actual_score) + ' Min_Score: ' + str(min_value) + ' Max_Score: ' + str(max_value))

    # TC1: Check Headers in all the CSV files
    def test_headers(self):
        csv_path = ENTITY_TO_PATH_DICT.values()
        for each_csv in csv_path:
        # Validate headers
            actual_headers = DataGenerationValidation.getting_header(each_csv, 'r')
            expected_headers = DataGenerationValidation.header_dict.get(os.path.basename(each_csv)[:-4])
            self.assertIsNotNone(expected_headers, ('No header info for %s' % each_csv))
            self.assertEqual(len(actual_headers), len(expected_headers), ('Number of header does not match: %s' % each_csv))
            for header in expected_headers:
                self.assertIn(header, actual_headers, ('Header Name: %s is missing in %s file' % (header, os.path.basename(each_csv)[:-4])))
        print('TC1: Passed: Check Headers in all the CSV files')

    # TC2: Validate min/Max assessment score, cut score and assessment performance level name
    def test_asmt_cut_level_score(self):
        with open(DataGenerationValidation.dim_asmt_csv, 'r') as csvfile:
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
    # dim_inst_hier--> school category/ school_id
    def test_grade(self):
        expected_school_category = ['High School', 'Middle School', 'Elementary School']
        with open(DataGenerationValidation.dim_inst_hier_csv, 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            dict = {}
            actual_school_category = []
            for school in col_val:
                all_school = school['school_category']
                # check the value is available in the List ot not if not add value in the list so we can compare with expected_school_categoty
                if all_school not in actual_school_category:
                    actual_school_category.append(all_school)
                school_id = school['school_id']
                # Get all the IDs for each school_categoty (High, Middle & Elementery) - without repeating school category
                if dict.get(all_school):
                    dict[all_school].append(school_id)
                else:
                    dict[all_school] = [school_id]
            # Comparing school category
            assert sorted(expected_school_category) == sorted(actual_school_category), 'School Category does not match'
        # get school_id from dim_section and check the grades
        csv_files = [DataGenerationValidation.fact_asmt_outcome_csv, DataGenerationValidation.dim_section_csv, DataGenerationValidation.dim_student_csv]
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
                        school_id = values['school_id']
                    else:
                        section_grade = values['asmt_grade']
                        school_id = values['school_id']
                    if section_grade in grade_dict:
                        if school_id not in grade_dict[section_grade]:
                            grade_dict[section_grade].append(school_id)
                    else:
                        grade_dict[section_grade] = [school_id]
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
                self.assertEqual(uniq_hi_list, overall_highschool, 'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4])
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
        with open(DataGenerationValidation.fact_asmt_outcome_csv, 'r') as csvfile:
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
        csv_files = [DataGenerationValidation.dim_inst_hier_csv, DataGenerationValidation.fact_asmt_outcome_csv,
                     DataGenerationValidation.dim_section_csv, DataGenerationValidation.dim_student_csv]
        for each_csv in csv_files:
            district_set = set()
            with open(each_csv, 'r') as csvfile:
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    district_id = values['district_id']
                    if district_id != 'NA':
                        district_set.add(district_id)

            assert DISTRICT_COUNT == len(district_set), 'District count in config file is ' + str(DISTRICT_COUNT) + ' but District count in ' + os.path.basename(each_csv)[:-4] + ' is ' + str(len(district_set))
        print('TC7: Passed: Count overall number of discticts from CSVs and compare with Config file')

    # TC8: Count number of schools from CSVs and compare with Config file
    def test_number_of_schools(self):
        state = get_state_types()[typical1]['district_types_and_counts']
        state_keys = list(get_state_types()[typical1]['district_types_and_counts'].keys())
        state_no = list(get_state_types()[typical1]['district_types_and_counts'].values())
        total_schools = 0
        final_total_schools = 0
        min_final_total = 0

        for index in range(len(state)):
            state_no1 = state_no[index]
            state_keys1 = state_keys[index]
            sum_dist_ratio = sum(get_district_types()[state_keys1]['school_types_and_ratios'].values())
            min_dist = get_district_types()[state_keys1]['school_counts']['min']
            dist_ratio = get_district_types()[state_keys1]['school_types_and_ratios'].values()
            total_schools = 0
            for each in dist_ratio:
                # min_dist_num = ((min_dist * each) // sum_dist_ratio)
                min_dist_num = max(((min_dist) * (each // sum_dist_ratio)), 1)
                total_schools += min_dist_num
            final_total = total_schools * state_no1
            min_final_total += final_total

#        typical1 = get_states()[0]['state_type']
#        district_type = get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS].keys()
#        school_type = get_district_types().keys()
#
#        min_schools = 0
#        max_schools = 0
#        for values in district_type:
#            if values in school_type:
#                min_district_num = (get_district_types()[values][SCHOOL_COUNTS][MIN]) * (get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS][values])
#                max_district_num = (get_district_types()[values][SCHOOL_COUNTS][MAX]) * (get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS][values])
#                min_schools += min_district_num
#                max_schools += max_district_num
        csv_files = [DataGenerationValidation.dim_inst_hier_csv, DataGenerationValidation.fact_asmt_outcome_csv,
                     DataGenerationValidation.dim_section_csv, DataGenerationValidation.dim_student_csv]
        for each_csv in csv_files:
            school_set = set()
            with open(each_csv, 'r') as csvfile:
                col_val = csv.DictReader(csvfile, delimiter=',')
                for values in col_val:
                    school_id = values['school_id']
                    if school_id != 'NA':
                        school_set.add(school_id)
#            assert min_schools <= len(school_set) <= max_schools, 'Min School count in config file is ' + str(min_schools) + ' Max School count in config file is ' + str(max_schools) + ' but School count in ' + os.path.basename(each_csv)[:-4] + ' is ' + str(len(school_set))
            assert min_final_total <= len(school_set), 'Min School count in config file is ' + str(min_final_total) + ' Max School count in config file is ' + 'but School count in ' + os.path.basename(each_csv)[:-4] + ' is ' + str(len(school_set))
        print('TC8: Passed: Count overall number of schools from CSVs and compare with Config file ')

    # TC9: Count number of students from CSVs and compare with Config file
    def test_number_of_students(self):
        min_total_num = 0
        max_total_num = 0
        final_min_total_num = 0
        final_max_total_num = 0
        typical1 = get_states()[0]['state_type']
        ratio_list = {}
        district_type_list = (list(get_district_types().keys()))
        district_type = sorted(district_type_list, reverse=True)

        for values in district_type:
            school_types_and_ratios_values = list(get_district_types()[values][SCHOOL_TYPES_AND_RATIOS].values())
            school_types_and_ratios_keys = list(get_district_types()[values][SCHOOL_TYPES_AND_RATIOS].keys())
            school_types_and_ratios_sum = sum(school_types_and_ratios_values)
            min_number_of_schools_in_district = get_district_types()[values][SCHOOL_COUNTS][MIN]
            for index in range(len(school_types_and_ratios_values)):
                values1 = school_types_and_ratios_values[index]
                keys1 = school_types_and_ratios_keys[index]
                min_school_count = ((min_number_of_schools_in_district // school_types_and_ratios_sum)) * values1

                grade_len = len(get_school_types()[keys1][GRADES])
                min_student = get_school_types()[keys1][STUDENTS][MIN] * grade_len
                min_total = min_school_count * min_student
                min_total_num += min_total
            overall_min_total_num = min_total_num * get_state_types()[typical1][DISTRICT_TYPES_AND_COUNTS][values]
            final_min_total_num += overall_min_total_num
        student_list = []
        with open(DataGenerationValidation.dim_student_csv, 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            for values in col_val:
                student_id = values['student_id']
                student_list.append(student_id)
        student_list = list(set(student_list))
        assert final_min_total_num <= len(student_list), 'Min Student count in config file is ' + str(final_min_total_num) + ' but Student count in is ' + str(len(student_list))
        print('TC9: Passed: Count overall number of students from CSVs and compare with Config file ')

    # TC10: Count Subjects & percentages
    def test_subjects_and_percentage(self):
        # Values from config file
        # Converting percentage value from float to integer by multiplying to check the value is in the range because range only works with integers
        math_percentage = int(get_state_types()[typical1]['subjects_and_percentages']['Math'] * 100)
        ela_percentage = int(get_state_types()[typical1]['subjects_and_percentages']['ELA'] * 100)
        both_count = 0
        math_only_count = 0
        ela_only_count = 0
        student_id_dict = {}
        math_guid = []
        ela_guid = []

        with open(DataGenerationValidation.dim_section_csv, 'r') as csvfile:
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
        with open(DataGenerationValidation.fact_asmt_outcome_csv, 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            for values in col_val:
                student_id = values['student_id']
                section_guid = values['section_guid']
                if student_id in student_id_dict:
                        student_id_dict[student_id].append(section_guid)
                else:
                    student_id_dict[student_id] = [section_guid]
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
        both_perc = round((1.0 * both_count / total_student_count), 2)
        # Converting percentage value from float to integer by multiplying to check the value is in the range because range only works with integers
        math_perc = int((round((1.0 * (both_count + math_only_count) / total_student_count), 2)) * 100)
        ela_perc = int((round((1.0 * (both_count + ela_only_count) / total_student_count), 2)) * 100)
        assert math_perc and ela_perc <= 100, 'More than 100% students have taken Math/ELA'
        assert math_perc in range((math_percentage - 4), (math_percentage + 4)), 'Math subject and percentage does not match. Expected ' + str(math_percentage / 100) + '(+/-0.04) but found ' + str(math_perc / 100)
        assert ela_perc in range((ela_percentage - 4), (ela_percentage + 4)), 'ELA subject and percentage does not match. Expected ' + str(ela_percentage / 100) + '(+/-0.04) but found ' + str(ela_perc / 100)
        print('TC10: Passed: Count Subjects & percentages ')

    # TC11: Check assessment type
    def test_assessment_type(self):
        with open(DataGenerationValidation.dim_asmt_csv, 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            for values in col_val:
                assessment_type = values['asmt_type']
                self.assertEqual(assessment_type, 'SUMMATIVE', 'Assessment type is incorrect in dim_asmt')
        print('TC11: Passed: Check assessment type')
