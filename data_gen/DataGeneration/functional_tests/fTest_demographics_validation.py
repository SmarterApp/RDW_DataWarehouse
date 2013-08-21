'''
Created on Aug 19, 2013

@author: swimberly
'''
import unittest
import csv
import os
import subprocess
import json
import sys

import DataGeneration.src.demographics as dmg
from DataGeneration.src.print_state_population import print_demographic_info

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

DIM_ASMT = 'dim_asmt.csv'
DIM_STUDENT = 'dim_student.csv'
DIM_SECTION = 'dim_section.csv'
DIM_STAFF = 'dim_staff.csv'
DIM_INST = 'dim_inst_hier.csv'
FACT_ASMT = 'fact_asmt_outcome.csv'
GRADE = 'asmt_grade'
TOTAL = 'total'
STUDENT_GUID = 'student_guid'
ALL = 'all'
PERF_LVL = 'asmt_perf_lvl'
ASMT_SUBJECT = 'asmt_subject'
ASMT_GUID = 'asmt_guid'
ASMT_REC_ID = 'asmt_rec_id'
MATH = 'Math'
ELA = 'ELA'
DEMO_STATS_CSV = os.path.join(__location__, '..', 'datafiles', 'demographicStats.csv')
DEMO_ID = 'typical1'
REGULAR_OUTPUT_PATH = os.path.join(__location__, '..', 'datafiles', 'csv')

DEMO_LIST = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
'''
Demographic Codes:
    0. dmg_eth_nst -- Not stated,
    1. dmg_eth_blk -- African American,
    2. dmg_eth_asn -- Asian,
    3. dmg_eth_hsp -- Hispanic,
    4. dmg_eth_ami -- Native American / Alaskan Native,
    5. dmg_eth_pcf -- Pacific Islander,
    6. dmg_eth_wht -- White,
    7. dmg_eth_2mr -- Two or more
'''
DERIVED_ETH_LIST = ['dmg_eth_nst', 'dmg_eth_blk', 'dmg_eth_asn', 'dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_eth_2mr']
DEMO_BY_GROUP = {'all': 0, 'male': 1, 'female': 1, 'not_stated': 1, 'dmg_eth_nst': 2, 'dmg_eth_blk': 2, 'dmg_eth_asn': 2, 'dmg_eth_hsp': 2,
                 'dmg_eth_ami': 2, 'dmg_eth_pcf': 2, 'dmg_eth_wht': 2, 'dmg_eth_2mr': 2, 'dmg_prg_iep': 3, 'dmg_prg_lep': 4, 'dmg_prg_504': 5, 'dmg_prg_tt1': 6}

REPORT_DEMO_SET = set(DEMO_LIST + DERIVED_ETH_LIST + [ALL])


class DemographicsFuncTest(unittest.TestCase):

    def f_test_generated_data_demographics(self):
        #output_location = run_data_generation()
        #fact_asmt_path = os.path.join(output_location, FACT_ASMT)
        #asmt_recs = get_asmt_rec_ids_by_subject(output_location)
        fact_asmt_path = os.path.join(REGULAR_OUTPUT_PATH, FACT_ASMT)
        asmt_recs = get_asmt_rec_ids_by_subject(REGULAR_OUTPUT_PATH)
        subject_counts_dict = self.get_demographic_counts_from_fact_csv(fact_asmt_path, asmt_recs)
        subject_percent_dict = convert_subject_counts_to_percentages(subject_counts_dict)
        #print(json.dumps(subject_percent_dict[MATH], indent=2))

        print_demographic_info(demo_totals=convert_subject_dict_for_printing(subject_percent_dict[MATH]))
        percent_diff = self.validate_math_percentages(subject_percent_dict)

        print_demographic_info(demo_totals=convert_subject_dict_for_printing(percent_diff))

    def get_demographic_counts_from_fact_csv(self, fact_asmt_path, asmt_rec_ids):
        with open(fact_asmt_path, 'r') as csv_file:
            c_reader = csv.DictReader(csv_file)
            count_dict = {MATH: {}, ELA: {}}

            # Loop through rows in the csv
            for row in c_reader:
                count_dict = self.analyze_fact_asmt_row(row, count_dict, asmt_rec_ids)
        #print(json.dumps(count_dict, indent=4))
        return count_dict

    def analyze_fact_asmt_row(self, row_dict, subject_count_dict, asmt_rec_id_dict):

        # pull out necessary info
        grade = row_dict[GRADE]
        perf_lvl = int(row_dict[PERF_LVL])
        asmt_guid = row_dict[ASMT_REC_ID]
        subject = MATH if asmt_guid in asmt_rec_id_dict[MATH] else ELA

        count_dict = subject_count_dict[subject]

        # Determine the demographics for this row
        row_demographics = find_demographics(row_dict)
        translated_row_demo = translate_row_demographics_list(row_demographics)

        # Check that dict has this grade
        if not count_dict.get(grade):
            count_dict[grade] = {demo: [0, 0, 0, 0, 0] for demo in REPORT_DEMO_SET}
        grade_counts = count_dict[grade]

        # increment total count
        grade_counts[ALL][0] += 1
        grade_counts[ALL][perf_lvl] += 1
        # loop demographics and add to the total count and the perf_lvl count for that demographic
        for demo in translated_row_demo:
            grade_counts[demo][0] += 1
            grade_counts[demo][perf_lvl] += 1

        return subject_count_dict

    def validate_math_percentages(self, subject_percent_dict):
        math_percentages = subject_percent_dict[MATH]
        demo_obj = dmg.Demographics(DEMO_STATS_CSV)
        subject_demographics = demo_obj.get_subject_demographics(DEMO_ID, MATH)

        percent_diff_dict = {}
        for grade in math_percentages:
            percent_diff_dict[grade] = {}
            for demo in math_percentages[grade]:
                percent_diff_dict[grade][demo] = []
                expected_total_perc = subject_demographics[grade][demo][dmg.L_TOTAL]
                resulting_percent = math_percentages[grade][demo][0]
                self.assertAlmostEqual(expected_total_perc, resulting_percent, places=None, delta=0.5)

                percent_diff_dict[grade][demo].append(determine_percent_difference((resulting_percent - expected_total_perc), expected_total_perc))
                for i in range(1, dmg.L_PERF_4):
                    result_pl_percent = math_percentages[grade][demo][i]
                    expected_pl_percent = subject_demographics[grade][demo][i + dmg.L_TOTAL]
                    #self.assertAlmostEqual(result_pl_percent, expected_pl_percent, delta=1, msg='Not Equal for grade %s, demo %s, perf level %s' % (grade, demo, i))
                    percent_diff_dict[grade][demo].append(determine_percent_difference((result_pl_percent - expected_pl_percent), expected_pl_percent))

        return percent_diff_dict


def determine_percent_difference(dividend, divisor):
    if divisor == 0:
        return 0
    return (dividend / divisor) * -100


def convert_subject_counts_to_percentages(subject_counts_dict):
    percents_by_subject = {}

    for subject in subject_counts_dict:
        counts_by_grade = subject_counts_dict[subject]
        percents_by_grade = {}

        for grade in counts_by_grade:
            grade_percentages = determine_demographic_percentages(counts_by_grade[grade])
            percents_by_grade[grade] = grade_percentages

        percents_by_subject[subject] = percents_by_grade

    return percents_by_subject


def determine_demographic_percentages(demographic_counts):
    demographic_percentages = {}
    total_students = demographic_counts[ALL][0]
    overall_percent_list = determine_percents_from_list(demographic_counts[ALL])
    demographic_percentages[ALL] = [100] + overall_percent_list[1:]

    for demo in demographic_counts:
        demo_list = demographic_counts[demo]
        percent_of_total = determine_percent_of_total(total_students, demo_list[0])
        percent_list = determine_percents_from_list(demo_list)
        demographic_percentages[demo] = [percent_of_total] + percent_list[1:]

    return demographic_percentages


def determine_percents_from_list(demographic_list):
    '''
    Given a list of values determine the percentage of the total for each value,
    where the first values in the total
    [total, val1, val2, val3, val4...]
    '''
    result_list = [0] * len(demographic_list)
    total = demographic_list[0]

    for i in range(1, len(demographic_list)):
        result_list[i] = determine_percent_of_total(total, demographic_list[i])

    return result_list


def determine_percent_of_total(total, value):
    if total == 0:
        return 0
    perc_decimal = value / total
    percent = perc_decimal * 100

    return percent


def get_asmt_rec_ids_by_subject(output_location):
    asmt_recs = {MATH: [], ELA: []}
    dim_asmt_path = os.path.join(output_location, DIM_ASMT)
    with open(dim_asmt_path, 'r') as c_file:
        c_reader = csv.DictReader(c_file)
        for row in c_reader:
            asmt_recs[row[ASMT_SUBJECT]].append(row[ASMT_REC_ID])
    return asmt_recs


def find_demographics(fact_row_dict):
    row_demographics = []
    for demo in DEMO_LIST:
        if fact_row_dict[demo] == 'True':
            row_demographics.append(demo)

    return row_demographics


def translate_row_demographics_list(row_demo_list):
    translated_list = []
    ethnicities = [x for x in row_demo_list if 'eth' in x]
    if len(ethnicities) > 1:
        if DERIVED_ETH_LIST[3] in ethnicities:
            translated_list.append(DERIVED_ETH_LIST[3])
        else:
            translated_list.append(DERIVED_ETH_LIST[7])
    elif len(ethnicities) == 0:
        translated_list.append(DERIVED_ETH_LIST[0])
    else:
        translated_list += ethnicities

    translated_list += [x for x in row_demo_list if 'eth' not in x]
    return translated_list


def convert_subject_dict_for_printing(subject_percent_dict):
    result_dict = {}
    for grade in subject_percent_dict:
        result_dict[int(grade)] = {}
        for demo in subject_percent_dict[grade]:
            result_dict[int(grade)][demo] = [DEMO_BY_GROUP[demo]] + subject_percent_dict[grade][demo]
    return result_dict


def run_data_generation():
    data_gen_loc = os.path.join(__location__, '..', 'src', 'generate_data.py')
    output_loc = os.path.join(__location__, 'test_output')
    config_file = 'dg_types'
    print('generating data for %s' % config_file)
    output = system('python', data_gen_loc, '--config', config_file, '--output', output_loc, '-N')
    sys.stdout.buffer.write(output)
    return output_loc


def system(*args, **kwargs):
    '''
    Method for running system calls
    Taken from the pre-commit file for python3 in the scripts directory
    '''
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _err = proc.communicate()
    return out


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
