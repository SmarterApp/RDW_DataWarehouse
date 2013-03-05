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
GENDER_RARIO = [0.5, 0.45, 0.55]

MIN_ASSMT_SCORE = 50
MAX_ASSMT_SCORE = 500

ASSMT_TYPES = {'Math':
               {'4':
                {'claim_names': ['Number properties and operations', 'Measurement and Geometry', 'Data analysis, statistics, and probability', 'Algebra'],
                 'claim_percs': [40, 35, 10, 15]},
                '8':
                {'claim_names': ['Number properties and operations', 'Measurement and Geometry', 'Data analysis, statistics, and probability', 'Algebra'],
                 'claim_percs': [20, 35, 15, 30]}
                },
               'ELA':
               {'4':
                {'claim_names': ['Literary text and Fiction', 'Literary nonfiction and Poetry', 'Informational text and Exposition', 'Argumentation and persuasive text'],
                 'claim_percs': [25, 25, 25, 25]},
                '8':
                {'claim_names': ['Literary text and Fiction', 'Literary nonfiction and Poetry', 'Informational text and Exposition', 'Argumentation and persuasive text'],
                 'claim_percs': [20, 25, 25, 30]}
                }
               }


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

DATE_YEAR_DIS = 10

MONTH_LIST_31DAYS = [1, 3, 5, 7, 8, 10, 12]
MONTH_LIST_30DAYS = [4, 6, 9, 11]
YEAR_SHIFT = 15
MONTH_TOTAL = 12
MONTH_DAY_MAX = [31, 30, 28]

HIER_USER_TYPE = ['Teacher', 'Staff']
