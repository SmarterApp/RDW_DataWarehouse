'''
constants.py

Contains many necessary constants for generating data
'''

ELEMENTARY_SCHOOL = 'Elementary School'
MIDDLE_SCHOOL = 'Middle School'
HIGH_SCHOOL = 'High School'
OTHER = 'Other'

SCHOOL_LEVELS_INFO = [[ELEMENTARY_SCHOOL, ['El Sch', 'Elem', 'Ctr', 'Elementary School', 'Primary', 'Elementary', 'Elem', 'Sch'], [[0, 5], [1, 5], [1, 6]]],
                      [MIDDLE_SCHOOL, ['Middle School', 'Community Middle', 'Middle', 'Junior High', 'Intermediate School', 'Jr Middle', 'MS'], [[6, 8], [5, 8], [7, 9]]],
                      [HIGH_SCHOOL, ['High Sch', 'High School', 'High', 'HS', 'Senior High'], [[9, 12], [10, 12]]],
                      [OTHER, ['Sch', 'School'], [[6, 12], [9, 12]]]
                      ]

SCHOOL_TYPE_TO_SUFFIXES = {ELEMENTARY_SCHOOL: ['El Sch', 'Elem', 'Ctr', 'Elementary School', 'Primary', 'Elementary', 'Elem', 'Sch'],
                           MIDDLE_SCHOOL: ['Middle School', 'Community Middle', 'Middle', 'Junior High', 'Intermediate School', 'Jr Middle', 'MS'],
                           HIGH_SCHOOL: ['High Sch', 'High School', 'High', 'HS', 'Senior High'],
                           OTHER: ['Sch', 'School']}

SCHOOL_ORDER_MAP = {ELEMENTARY_SCHOOL: 0, MIDDLE_SCHOOL: 1, HIGH_SCHOOL: 2, OTHER: 3}
SCHOOL_TYPES = ['Alternative', 'Regular', 'Special Education', 'Vocational', 'JJAEP', 'DAEP']

DISTRICT_SUFFIX = ['District', 'School District', 'Schools', 'County Schools', 'Public Schools', 'SD']
ADD_SUFFIX = ["ROAD", "AVE", "STREET", "PARKWAY", "BLVD", "WAY"]

SUBJECTS = ["Math", "ELA"]
MATH = SUBJECTS[0]
ELA = SUBJECTS[1]

GENDERS = ['male', 'female']

MIN_CLASS_SIZE = 20
MIN_SECTION_SIZE = 10

NUMBER_OF_SECTIONS = 1
STAFF_PER_SECTION = 1
NUMBER_OF_DISTRICT_LEVEL_STAFF = 10

MINIMUM_ASSESSMENT_SCORE = 1200
MAXIMUM_ASSESSMENT_SCORE = 2400
AVERAGE_ASSESSMENT_SCORE = (MINIMUM_ASSESSMENT_SCORE + MAXIMUM_ASSESSMENT_SCORE) / 2
ASSESSMENT_SCORE_STANDARD_DEVIATION = (AVERAGE_ASSESSMENT_SCORE - MINIMUM_ASSESSMENT_SCORE) / 4

# Different assessments have different numbers of claims.  The claims are defined with this dictionary
# It is used during the creation of 'assessment' objects.
CLAIM_DEFINITIONS = {'Math': [{'claim_name': 'Concepts & Procedures', 'claim_weight': .4},
                              {'claim_name': 'Problem Solving and Modeling & Data Analysis', 'claim_weight': .45},
                              {'claim_name': 'Communicating Reasoning', 'claim_weight': .15}
                              ],
                     'ELA': [{'claim_name': 'Reading', 'claim_weight': .20},
                             {'claim_name': 'Writing', 'claim_weight': .25},
                             {'claim_name': 'Listening', 'claim_weight': .25},
                             {'claim_name': 'Research & Inquiry', 'claim_weight': .30}]
                     }
CLAIM_SCORE_MASTER_MIN = 10
CLAIM_SCORE_MASTER_MAX = 99

ASMT_PERF_CHANGE_MIN = 75
ASMT_PERF_CHANGE_MAX = 500

ZIPCODE_START = 10000
ZIPCODE_RANG_INSTATE = 5000

INST_CATEGORIES = ['State Education Agency', 'Education Service Center', 'Local Education Agency', 'School']

STAT_COLUMNS = ['state_code', 'state_name', 'total_district', 'total_school', 'total_student', 'total_teacher',
                'min_school_per_district', 'max_school_per_district', 'std_school_per_district', 'avg_school_per_district',
                'min_student_per_school', 'max_student_per_school', 'std_student_per_school', 'avg_student_per_school',
                'min_stutea_ratio_per_school', 'max_stutea_ratio_per_school', 'std_stutea_ratio_per_school', 'avg_stutea_ratio_per_school',
                'primary_perc', 'middle_perc', 'high_perc', 'other_perc']

RETRY_CAL_STAT = 100
DIST_LOW_VALUE = 0.9
DIST_HIGH_VALUE = 1.2

DIST_SCHOOL_NAME_LENGTH = 256
CITY_NAME_LENGTH = 100
ADDRESS_LENGTH = 256

HIER_USER_TYPE = ['Teacher', 'Staff']

SCORE_MIN_MAX_RANGE = 20

ASSMT_SCORE_YEARS = [2015]
ASSMT_TYPES = ['SUMMATIVE']
ASSMT_PERIODS = ['Fall', 'Spring']
ASSMT_PERIOD_TO_MONTHS_DICT = {'Fall': [9, 10, 11, 12], 'Spring': [1, 2, 3, 4, 5]}
PERFORMANCE_LEVELS = ['Minimal Understanding', 'Partial Understanding', 'Adequate Understanding', 'Thorough Understanding']

CLAIM_PERFORMANCE_LEVELS = ['Below Standard', 'At/Near Standard', 'Above Standard']

HISPANIC_CODE = 3
TWO_OR_MORE_RACES_CODE = 7

# DG_TYPES CONSTANTS
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
CLAIM_CUT_POINTS = 'claim_cut_points'
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
