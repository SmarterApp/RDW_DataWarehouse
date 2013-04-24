'''
Created on Apr 4, 2013

@author: kallen
'''

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


def get_school_types():
    """
    structure: {school-type: {'grades': val, 'students': {'min': val, 'max': val, 'avg': val}},...}
    where school-type is High, Middle, Elementary
    grades is a list of grades for that type
    students is a dictionary containing the min, max and avg number of students
    """
    school_types = {'High School': {'grades': [11], 'students': {'min': 100, 'max': 500, 'avg': 300}},
                    'Middle School': {'grades': [6, 7, 8], 'students': {'min': 50, 'max': 200, 'avg': 150}},
                    'Elementary School': {'grades': [3, 4, 5], 'students': {'min': 20, 'max': 70, 'avg': 60}}
                   }
    return school_types


def get_district_types():
    """
    structure: {district-type: {'school_counts': {'min': val, 'max': val, 'avg': val}, 'school_types_and_ratios': {'High': val, 'Middle': val, 'Elementary': val},...}
    where district-type is Big, Medium or Small
    'school_counts' is a dictionary that describes the min, max and avg for that school_type
    'school_types_and_ratios' is dictionary containing the ratios of High to Middle to Elementary schools
    (ie. 1:2:5 -- {'High': 1, 'Middle': 2, 'Elementary': 5})
    """
<<<<<<< Updated upstream:DataGeneration/src/dg_types.py
    district_types = {'Big': {'school_counts': {'min': 50, 'max': 80, 'avg': 65}, 'school_types_and_ratios': {'High School': 1, 'Middle School': 2, 'Elementary School': 5}},
                     'Medium': {'school_counts': {'min': 20, 'max': 24, 'avg': 22}, 'school_types_and_ratios': {'High School': 1, 'Middle School': 2, 'Elementary School': 5}},
                     'Small': {'school_counts': {'min': 2, 'max': 8, 'avg': 5}, 'school_types_and_ratios': {'High School': 1, 'Middle School': 2, 'Elementary School': 5}}
=======
    district_types = {'Big'      : { 'school_counts' : {'min' : 50, 'max' : 80, 'avg' : 65}, 'school_types_and_ratios' : {'High School' : 1, 'Middle School' : 2, 'Elementary School' : 5} },
                     'Medium'   : { 'school_counts' : {'min' : 20, 'max' : 50, 'avg' : 22}, 'school_types_and_ratios' : {'High School' : 1, 'Middle School' : 2, 'Elementary School' : 5} },
                     'Small'    : { 'school_counts' : {'min' :  2, 'max' :  8, 'avg' :  5}, 'school_types_and_ratios' : {'High School' : 1, 'Middle School' : 2, 'Elementary School' : 5} }
>>>>>>> Stashed changes:DataGeneration/src/config_file_data_generation/dg_types.py
                     }
    return district_types


def get_state_types():
    """
    structure: {state-type: {'district_types_and_counts': {'Big': val, 'Medium': val, 'Small': val}, 'subjects_and_percentages': {'Math': val, 'ELA': val}
    where state-type is the type of state
    'district_types_and_counts' is a dictionary that describes how many Big, Medium and Small districts to have in the state
    'subjects_and_percentages' is a dictionary that describes what percentage of students should have scores for a Math assessment and an ELA assessment
    """
    state_types = {'typical_1': {'district_types_and_counts': {'Big': 2, 'Medium': 6, 'Small': 40}, 'subjects_and_percentages': {'Math': .9, 'ELA': .9}}
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
    states = [{'name': 'Example State', 'state_code': 'ES', 'state_type': 'typical_1'}]
    return states


def get_scores():
    """
    min + max + 3 cut points define 4 pereformance levels
    PL1 = min - cp1 (exclusive)
    PL2 = cp1 - cp2 (exclusive)
    PL3 = cp2 - cp3 (exclusive)
    PL4 = cp3 - max (inclusive)
    """
    scores = {'min': 1200, 'max': 2400, 'cut_points': [1400, 1800, 2100]}
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
                    '11': {'percentages': [26, 37, 28, 9]}}
                    }
    return pld


def get_temporal_information():
    temporal_information = {'from_date': '20120901', 'to_date': None, 'most_recent': True, 'date_taken_year': '2012', 'date_taken_month': ''}
    return temporal_information
