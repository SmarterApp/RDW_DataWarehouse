import unittest
import csv
import os
import entities_2 as entities
import itertools
from generate_data import ENTITY_TO_PATH_DICT
from zope.component.tests.examples import comp
import dg_types


GRADES = 'grades'
STUDENTS = 'students'
STATE_TYPE = 'stateType'
DISTRICT_TYPES_AND_COUNTS = 'districtTypesAndCounts'


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
    def dict_reader (file_path, file_format):
        with open (file_path) as csvFile:
            fileValue = csv.DictReader(csvFile, delimiter =',' )
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
            with open ('./datafiles/csv/fact_asmt_outcome.csv', 'r') as csvfile:
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
                    
                    assert 1200 <= actual_score and min_value and max_value <= 2400, ('Incorrect score: Actual score: '+ str(actual_score) + ' Min_Score: ' + str(min_value) + ' Max_Score: ' + str(max_value))
                    if min_value != 1200 and max_value != 2400:
                        assert (actual_score - min_value) == (max_value - actual_score) , ('Min/Max scores are not in range in fact_asmt_outcome file. Actual score: '+ str(actual_score) + ' Min_Score: ' + str(min_value) + ' Max_Score: ' + str(max_value))
                
    
    # TC1: Check Headers in all the CSV files.

    #class_names = ENTITY_TO_PATH_DICT
   
    def test_headers(self):
        csv_path = ENTITY_TO_PATH_DICT.values()
        for each_csv in csv_path:
        # do validate
            actual_headers = DataGenerationValidation.getting_header(each_csv, 'r')
            expected_headers = DataGenerationValidation.header_dict.get(os.path.basename(each_csv)[:-4])
        
        
            assert expected_headers is not None,('No header info for %s' % each_csv)
            assert len(actual_headers) == len(expected_headers),('Number of header does not match: %s' % each_csv)
            for header in expected_headers:
                assert header in actual_headers,('Header Name: %s is missing in %s file' %(header, os.path.basename(each_csv)[:-4]))
        print('TC1: Passed: Check Headers in all the CSV files')
            
            
    # TC2: Validate min/Max assessment score, cut score and assessment performance level names
    
    def test_asmt_cut_lavel_score(self):
    
        with open('./datafiles/csv/dim_asmt.csv', 'r') as csvfile:
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
                
    
            asmt_dict = {'asmt_score_min': [int(asmt_score_min), 1200],
                         'asmt_score_max': [int(asmt_score_max), 2400],
                         'asmt_cut_point_1': [int(asmt_cut_point_1), 1400],
                         'asmt_cut_point_2': [int(asmt_cut_point_2), 1800],
                         'asmt_cut_point_3': [int(asmt_cut_point_3), 2100],
                         'asmt_cut_point_4': [(asmt_cut_point_4), ''],
                         'asmt_perf_lvl_name_1': [(asmt_perf_lvl_name_1), 'Minimal Understanding'],
                         'asmt_perf_lvl_name_2': [(asmt_perf_lvl_name_2), 'Partial Understanding'],
                         'asmt_perf_lvl_name_3': [(asmt_perf_lvl_name_3), 'Adequate Understanding'],
                         'asmt_perf_lvl_name_4': [(asmt_perf_lvl_name_4), 'Thorough Understanding']}
                         
            for key, value in asmt_dict.items():
                    csv_asmt_value = value[0]
                    config_asmt_value = value[1]
                    assert csv_asmt_value == config_asmt_value, (key + ' value is incorrect. Expected ', config_asmt_value , ' but found ', csv_asmt_value)
        print('TC2: Passed: Validate min/Max assessment score, cut score and assessment performance level names')

    # TC3: Validate School Categoty

    # dim_inst_hier--> school category/ school_guid
    def test_grade(self):
        expected_school_category = ['High School', 'Middle School', 'Elementary School']
                
        with open('./datafiles/csv/dim_inst_hier.csv', 'r') as csvfile:
            col_val = csv.DictReader(csvfile, delimiter=',')
            dict = {}
            actual_school_category = []
            for school in col_val:
                all_school = school ['school_category']
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
            
            # Comapring school category
            assert sorted(expected_school_category) == sorted(actual_school_category), 'School Category does not match'
               
        # get school_guid from dim_section and check the grades
        csv_files = ['./datafiles/csv/fact_asmt_outcome.csv','./datafiles/csv/dim_section.csv', './datafiles/csv/dim_student.csv']
        for each_file in csv_files:
            with open(each_file, 'r') as csvfile:
                
                grade_dict = {}
                sec_dic = {}
                expexted_grade = ['3','4','5','6','7','8','11']
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
                assert sorted(expexted_grade) == sorted(actual_grade), ('Expected Grades:',  sorted(expexted_grade), 'but found:', sorted(actual_grade), 'in', os.path.basename(each_file)[:-4]) 
                
            # High school - Grades from dim_section
                uniq_hi_list = []
                overall_highschool_list = grade_dict['11']
                overall_highschool_list_int = list(map(int, overall_highschool_list))
                overall_highschool_list_int.sort(key=None, reverse=False)
                for values in overall_highschool_list_int:
                    if values not in uniq_hi_list:
                        uniq_hi_list.append(values)
                
                # High school - School category from dim_inst_hier
                overall_highschool = dict['High School']
                overall_highschool_int = list(map(int, overall_highschool))
                
                
                # Validate Grades according to the school category
                assert uniq_hi_list == overall_highschool_int,'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4] 
                  
            
            # Middle School
            uniq_ml_list = []
            overall_middleschool_list = grade_dict['6'] + grade_dict['7'] + grade_dict['8']
            overall_middleschool_list_int = list(map(int, overall_middleschool_list))
            overall_middleschool_list_int.sort(key=None, reverse=False)
            for values in overall_middleschool_list_int:
                if values not in uniq_ml_list:
                    uniq_ml_list.append(values)             
        
            overall_middleschool = dict['Middle School']
            overall_middleschool_int = list(map(int, overall_middleschool))
            
            
            assert uniq_ml_list == overall_middleschool_int,'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4]
               
                
            # Elementary School
            uniq_el_list = []
            overall_elementaryschool_list = grade_dict['3'] + grade_dict['4'] + grade_dict['5']
            overall_elementaryschool_list_int = list(map(int, overall_elementaryschool_list))
            overall_elementaryschool_list_int.sort(key=None, reverse=False)
            for values in overall_elementaryschool_list_int:
                if values not in uniq_el_list:
                    uniq_el_list.append(values)
        
            overall_elementaryschool = dict['Elementary School']
            overall_elementaryschool_int = list(map(int, overall_elementaryschool))
            
            assert uniq_el_list == overall_elementaryschool_int,'SchoolIDs or Grades are incorrect in ' + os.path.basename(each_file)[:-4]
        print('TC3: Passed: Validate School Categoty and grades respect to School Category') 

    # TC4: Check Ids are not empty in all CSVs
    def test_primary_key(self):
    #        class_names = ENTITY_TO_PATH_DICT
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
                DataGenerationValidation.score_fact_asmt(score_part[0],score_part[1],score_part[2])

            print('Tc5: Passed: Validate scores in fact_asmt_outcome file')


    # TC6: check assessment performance level in fact_asmt_outcome
    
    def test_performence_level(self):
    
            perf_lvl = []
            asmt_score_list = []
            with open ('./datafiles/csv/fact_asmt_outcome.csv', 'r') as csvfile:
                        col_val = csv.DictReader(csvfile, delimiter=',') 
                        for values in col_val:
                            asmt_perf_lvl = values['asmt_perf_lvl']
                            perf_lvl.append(asmt_perf_lvl)
                            asmt_score = values['asmt_score']
                            asmt_score_list.append(asmt_score)
                        
                        for i in range(len(asmt_score_list)):
                            if 1200<=(int(asmt_score_list[i]))<=1399 and (int(perf_lvl[i])) == 1:
                                pass
                            elif 1400<=(int(asmt_score_list[i]))<=1799 and (int(perf_lvl[i])) == 2:
                                pass
                            elif 1800<=(int(asmt_score_list[i]))<=2099 and (int(perf_lvl[i])) == 3:
                                pass
                            elif 2100<=(int(asmt_score_list[i]))<=2400 and (int(perf_lvl[i])) == 4:
                                pass
                            else:
                               raise AssertionError('Fail: fact_asmt_outcome file. Asseessment score:' + asmt_score_list[i] +  ' and Performance_level:' + perf_lvl[i])
            print('TC6: Passed: Validate Performance level in fact_asmt_outcome file')
