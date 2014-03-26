import os

DATAFILE_PATH = str(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

BIRDS_FILE = DATAFILE_PATH + "/datafiles/name_lists/birds.txt"
MAMMALS_FILE = DATAFILE_PATH + "/datafiles/name_lists/mammals.txt"
FISH_FILE = DATAFILE_PATH + "/datafiles/name_lists/fish.txt"

SCHOOL_LEVELS_INFO = [['Elementary School', ['EL SCH', 'ELEM', 'CTR', 'ELEMENTARY SCHOOL', 'PRIMARY', 'ELEMENTARY', 'ELEM', 'SCH'], [[0, 5], [1, 5], [1, 6]]],
                      ['Middle School', ['MIDDLE SCHOOL', 'COMMUNITY MIDDLE', 'MIDDLE', 'JUNIOR HIGH', 'INTERMEDIATE SCHOOL', 'JR MIDDLE', 'MS'], [[6, 8], [5, 8], [7, 9]]],
                      ['High School', ['HIGH SCH', 'HIGH SCHOOL', 'HIGH', 'HS', 'SENIOR HIGH'], [[9, 12], [10, 12]]],
                      ['Other', ['SCH', 'SCHOOL'], [[6, 12], [9, 12]]]
                      ]


SCHOOL_ORDER_MAP = {'Elementary School': 0, 'Middle School': 1, 'High School': 2, 'Other': 3}
SCHOOL_TYPES = ['Alternative', 'Regular', 'Special Education', 'Vocational', 'JJAEP', 'DAEP']

DIST_SUFFIX = ['DISTRICT', 'SCHOOL DISTRICT', 'SCHOOLS', 'COUNTY SCHOOLS', 'PUBLIC SHCOOLS', 'SD']
ADD_SUFFIX = ["ROAD", "AVE", "STREET", "SOUTH AVE", "NORTH AVE", "WAY"]

SUBJECTS = ["Math", "ELA"]

MIN_CLASS_SIZE = 20
MIN_SECTION_SIZE = 10

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
                             {'claim_name': 'Speaking & Listening', 'claim_weight': .25},
                             {'claim_name': 'Research & Inquiry', 'claim_weight': .30}]
                     }
CLAIM_SCORE_MASTER_MIN = 10
CLAIM_SCORE_MASTER_MAX = 99

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

ASSMT_SCORE_YEARS = [2012]
