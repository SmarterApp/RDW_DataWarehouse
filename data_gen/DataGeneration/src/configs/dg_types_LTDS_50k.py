'''
Created on Apr 4, 2013

@author: kallen
'''

import os

GRADES = 'grades'
STUDENTS = 'students'
STATE_TYPE = 'state_type'
DISTRICT_TYPES_AND_COUNTS = 'district_types_and_counts'
SCHOOL_COUNTS = 'school_counts'
MIN = 'min'
AVG = 'avg'
MAX = 'max'
SCHOOL_TYPES_AND_RATIOS = 'school_types_and_ratios'
NAME = 'name'
PERCENTAGES = 'percentages'
GAMMA = 'gamma'
STD = 'std'
STATE_CODE = 'state_code'
CUT_POINTS = 'cut_points'
MIN_PERC = 'min_divisor'
MAX_PERC = 'max_divisor'
RAND_ADJ_PNT_LO = 'random_adjustment_points_lo'
RAND_ADJ_PNT_HI = 'random_adjustment_points_hi'
FROM_DATE = 'from_date'
TO_DATE = 'to_date'
MOST_RECENT = 'most_recent'
SUBJECT_AND_PERCENTAGES = 'subjects_and_percentages'
TYPE = 'type'
ADJUST_PLD = 'adjust_pld'
DEMOGRAPHICS = 'demographics'


def get_school_types():
    """
    structure: {school-type: {'grades': val, 'students': {'min': val, 'max': val, 'avg': val}},...}
    where school-type is High, Middle, Elementary
    grades is a list of grades for that type
    students is a dictionary containing the min, max and avg number of students
    """
    school_types = {
        'High School': {'type': 'High School', 'grades': [11], 'students': {'min': 10, 'max': 30, 'avg': 20}},
        'Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 10, 'max': 30, 'avg': 20}},
        'Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 5, 'max': 15, 'avg': 10}},

        'Poor High School': {'type': 'High School', 'grades': [11], 'students': {'min': 10, 'max': 30, 'avg': 20}, 'adjust_pld': -0.45},
        'Poor Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 10, 'max': 30, 'avg': 20}, 'adjust_pld': -0.5},
        'Poor Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 5, 'max': 15, 'avg': 10}, 'adjust_pld': -0.6},

        'Good High School': {'type': 'High School', 'grades': [11], 'students': {'min': 10, 'max': 30, 'avg': 20}, 'adjust_pld': 0.35},
        'Good Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 10, 'max': 30, 'avg': 20}, 'adjust_pld': 0.4},
        'Good Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 5, 'max': 15, 'avg': 10}, 'adjust_pld': 0.5},
    }

    return school_types

# District sizes : min/max/avg schools per type of district
SML_MIN = 3
SML_MAX = 2 * SML_MIN
SML_AVG = int((SML_MAX + SML_MIN) / 2)

MED_MIN = 2 * SML_MIN  # if small min =  5 then medium min = 20
MED_MAX = 2 * SML_MAX  # if small max = 10 then medium max = 40
MED_AVG = int((MED_MAX + MED_MIN) / 2)

BIG_MIN = 2 * MED_MIN  # if medium min = 20 then big min =  80
BIG_MAX = 2 * MED_MAX  # if medium max = 40 then big max = 160
BIG_AVG = int((BIG_MAX + BIG_MIN) / 2)

# School ratios
BASE_HIGH = 1
BASE_MIDL = 2
BASE_ELEM = 5
# ratios for 'average' schools
NORM_HIGH = 4 * BASE_HIGH
NORM_MIDL = 4 * BASE_MIDL
NORM_ELEM = 4 * BASE_ELEM
# ratios for 'featured' schools (good schools in good districts, poor schools in poor districts)
FEAT_HIGH = 6 * BASE_HIGH
FEAT_MIDL = 6 * BASE_MIDL
FEAT_ELEM = 6 * BASE_ELEM
# ratios for 'other' schools (poor schools in good districts, good schools in poor districts)
OTHR_HIGH = 1 * BASE_HIGH
OTHR_MIDL = 1 * BASE_MIDL
OTHR_ELEM = 1 * BASE_ELEM

VERY_NORM_HIGH = 3 * BASE_HIGH
VERY_NORM_MIDL = 3 * BASE_MIDL
VERY_NORM_ELEM = 3 * BASE_ELEM

VERY_FEAT_HIGH = 7 * BASE_HIGH
VERY_FEAT_MIDL = 7 * BASE_MIDL
VERY_FEAT_ELEM = 7 * BASE_ELEM

"""
LTDS = Load Testing data set. Used by QA for UDL load testing.

Need to generate here:
Approximately 50k Fact Assessment Outcome Records

"""


def get_district_types():
    """
    structure: {district-type: {'school_counts': {'min': val, 'max': val, 'avg': val}, 'school_types_and_ratios': {'High': val, 'Middle': val, 'Elementary': val},...}
    where district-type is Big, Medium or Small
    'school_counts' is a dictionary that describes the min, max and avg for that school_type
    'school_types_and_ratios' is dictionary containing the ratios of High to Middle to Elementary schools
    (ie. 1:2:5 -- {'High': 1, 'Middle': 2, 'Elementary': 5})

    """
    district_types = {'Big Average': {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},  # if SML_MIN = 5 then (80, 160, 120)
                                      'school_types_and_ratios': {
                                          'High School': NORM_HIGH, 'Middle School': NORM_MIDL, 'Elementary School': NORM_ELEM}},

                      'Medium Average': {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},  # if SML_MIN = 5 then (20, 40, 30)
                                         'school_types_and_ratios': {
                                             'High School': NORM_HIGH, 'Middle School': NORM_MIDL, 'Elementary School': NORM_ELEM}},

                      'Small Average': {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},  # if SML_MIN = 5 then (5, 10, 7)
                                        'school_types_and_ratios': {
                                            'High School': NORM_HIGH, 'Middle School': NORM_MIDL, 'Elementary School': NORM_ELEM}}
                      }
    return district_types


def get_state_types():
    """
    structure: {state-type: {'district_types_and_counts': {'Big': val, 'Medium': val, 'Small': val}, 'subjects_and_percentages': {'Math': val, 'ELA': val}
    where state-type is the type of state
    'district_types_and_counts' is a dictionary that describes how many Big, Medium and Small districts to have in the state
    'subjects_and_percentages' is a dictionary that describes what percentage of students should have scores for a Math assessment and an ELA assessment

    Initial numbers were Big=3, Medium=6, Small=40
    """
    state_types = {'LTDS': {'district_types_and_counts': {'Big Average': 25, 'Medium Average': 25, 'Small Average': 25}, 'subjects_and_percentages': {'Math': .99, 'ELA': .99}, 'demographics': 'typical1'}
                   }
    return state_types


def get_states():
    """
    Structure:
    {'name': val, 'state_code': val, 'state_type': val}
    where 'name' is the name of the state (eg. New York)
    'state_code' is the code for that state (eg. NY)
    'state_type' is the type of the state. This should match something that has been defined in get_state_types()
    """
    states = [{'name': 'New York', 'state_code': 'NY', 'state_type': 'LTDS'}]
    return states


def get_scores():
    """
    min + max + 3 cut points define 4 performance levels
    PL1 = min - cp1 (exclusive)
    PL2 = cp1 - cp2 (exclusive)
    PL3 = cp2 - cp3 (exclusive)
    PL4 = cp3 - max (inclusive)
    """
    scores = {'min': 1200, 'max': 2400, 'cut_points': [1400, 1800, 2100], 'claim_cut_points': [1600, 2000]}
    return scores


def get_error_band():
    """
    Error Band information
    Structure of dictionary: {'min_%': val, 'max_%': val, 'random_adjustment_points_lo': val, 'random_adjustment_points_hi': val}
    where 'min_divisor' is the divisor of the minimum fraction of the error band. At the center of the score range, the error band should be at this value (ie 1/32)
    'max_divisor' is the divisor of the maximum fraction of the error band. At each extreme of the score range, the error band should be at this value (ie 1/8)
    'random_adjustment_points_lo' is the lower bound for getting the random adjustment
    'random_adjustment_points_hi' is the upper bound for getting the random adjustment
    """
    eb = {'min_divisor': 32, 'max_divisor': 8, 'random_adjustment_points_lo': -10, 'random_adjustment_points_hi': 25}
    return eb


def get_performance_level_distributions():
    """
    Structure is :
    {'assessment-type' : {'grade': {'algorithm': algorithm-parameters}}}
    where 'algorithm' is one of 'percentages' or 'gamma'
    the nature of 'algorithm-parameters' depends on the choice of algorithm
    'percentages': [list of numbers summing to 100]
    'gamma': {'avg': average-value, 'std': standard-deviation} optionally can also have 'min' and 'max' values
    """

    pld = {'ELA': {'3': {'percentages': [30, 34, 28, 9]},
                   '4': {'percentages': [29, 36, 28, 7]},
                   '5': {'percentages': [27, 38, 29, 6]},
                   '6': {'percentages': [26, 39, 29, 6]},
                   '7': {'percentages': [25, 40, 30, 5]},
                   '8': {'percentages': [23, 42, 31, 4]},
                   '11': {'percentages': [21, 44, 32, 3]}
                   },
           'Math': {'3': {'percentages': [14, 42, 37, 7]},
                    '4': {'percentages': [16, 42, 35, 7]},
                    '5': {'percentages': [18, 41, 33, 8]},
                    '6': {'percentages': [20, 40, 31, 9]},
                    '7': {'percentages': [22, 39, 30, 9]},
                    '8': {'percentages': [24, 38, 29, 9]},
                    '11': {'percentages': [26, 37, 28, 9]}
                    }
           }
    return pld


def get_temporal_information():
    temporal_information = {'from_date': '20120901', 'to_date': None, 'most_recent': True, 'date_taken_year': '2015', 'date_taken_month': ''}
    return temporal_information


def get_demograph_file():
    datafile_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(datafile_path, '..', '..', 'datafiles', 'demographicStats.csv')

if __name__ == "__main__":
    print("in dg_types.py")
