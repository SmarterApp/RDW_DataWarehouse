import os

DATAFILE_PATH = str(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

BIRDS_FILE = DATAFILE_PATH + "/datafiles/name_lists/birds.txt"
MAMMALS_FILE = DATAFILE_PATH + "/datafiles/name_lists/mammals.txt"
FISH_FILE = DATAFILE_PATH + "/datafiles/name_lists/fish.txt"

SCHOOL_LEVELS_INFO = [
                    ['Primary', ['EL SCH', 'ELEM', 'CTR', 'ELEMENTARY SCHOOL', 'PRIMARY', 'ELEMENTARY', 'CETR, ELEM', 'SCH'], [[0, 5], [1, 5], [1, 6]]],
                    ['Middle', ['MIDDLE SCHOOL', 'COMMUNITY MIDDLE', 'MIDDLE', 'JUNIOR HIGH', 'INTERMEDIATE SCHOOL', 'JR MIDDLE', 'MS'], [[6, 8], [5, 8], [7, 9]]],
                    ['High', ['HIGH SCH', 'HIGH SCHOOL', 'HIGH', 'HS', 'SENIOR HIGH'], [[9, 12], [10, 12]]],
                    ['Other', ['SCH', 'SCHOOL'], [[6, 12], [9, 12]]]
                    ]

DIST_SUFFIX = ['DISTRICT', 'SCHOOL DISTRICT', 'SCHOOLS', 'COUNTY SCHOOLS', 'PUBLIC SHCOOLS', 'SD']
ADD_SUFFIX = ["ROAD", "AVE", "STREET", "SOUTH AVE", "NORTH AVE", "WAY"]

SUBJECTS = ["Math", "ELA"]
MIN_CLASS_SIZE = 20
MIN_SECTION_SIZE = 10
GENDER_RARIO = [0.5, 0.45, 0.55]

MIN_ASSMT_SCORE = 50
MAX_ASSMT_SCORE = 500

ASSMT_TYPES = {'Math': {
                       '4': {
                             'claim_names': ['Number properties and operations', 'Measurement and Geometry', 'Data analysis, statistics, and probability', 'Algebra'],
                             'claim_percs': [40, 35, 10, 15]
                             },
                        '8': {
                             'claim_names': ['Number properties and operations', 'Measurement and Geometry', 'Data analysis, statistics, and probability', 'Algebra'],
                             'claim_percs': [20, 35, 15, 30]
                             }

                        },
               'ELA': {
                       '4': {
                             'claim_names': ['Literary text and Fiction', 'Literary nonfiction and Poetry', 'Informational text and Exposition', 'Argumentation and persuasive text'],
                             'claim_percs': [25, 25, 25, 25]
                             },
                        '8': {
                             'claim_names': ['Literary text and Fiction', 'Literary nonfiction and Poetry', 'Informational text and Exposition', 'Argumentation and persuasive text'],
                             'claim_percs': [20, 25, 25, 30]
                             }
                        }
                }


# Output files for use in write_to_csv.py and generate data.py
STATES = DATAFILE_PATH + '/datafiles/csv/states.csv'
DISTRICTS = DATAFILE_PATH + '/datafiles/csv/districts.csv'
SCHOOLS = DATAFILE_PATH + '/datafiles/csv/schools.csv'
PARENTS = DATAFILE_PATH + '/datafiles/csv/parents.csv'
ASSESSMENT_TYPES = DATAFILE_PATH + '/datafiles/csv/assessment_types.csv'
ASSESSMENT_OUTCOME = DATAFILE_PATH + '/datafiles/csv/assessment_outcome.csv'
HIST_ASSESSMENT_OUTCOME = DATAFILE_PATH + '/datafiles/csv/hist_assessment_outcome.csv'
STUDENT_SECTIONS = DATAFILE_PATH + '/datafiles/csv/stu_sections.csv'
TEACHER_SECTIONS = DATAFILE_PATH + '/datafiles/csv/tea_sections.csv'
TEACHERS = DATAFILE_PATH + '/datafiles/csv/teachers.csv'
CLASSES = DATAFILE_PATH + '/datafiles/csv/classes.csv'
SECTIONS = DATAFILE_PATH + '/datafiles/csv/sections.csv'
STUDENTS = DATAFILE_PATH + '/datafiles/csv/students.csv'
WHERETAKEN = DATAFILE_PATH + '/datafiles/csv/wheretaken.csv'
INSTITUTIONS = DATAFILE_PATH + '/datafiles/csv/institutions.csv'

ENT_LIST = [STATES, PARENTS, ASSESSMENT_TYPES, STUDENT_SECTIONS, TEACHER_SECTIONS, CLASSES, SECTIONS, STUDENTS, WHERETAKEN, INSTITUTIONS, TEACHERS, ASSESSMENT_OUTCOME, HIST_ASSESSMENT_OUTCOME]

ZIPCODE_START = 10000
ZIPCODE_RANG_INSTATE = 5000

INST_CATEGORIES = ['State Education Agency', 'Education Service Center', 'Local Education Agency', 'School']

STAT_COLUMNS = ['state_code', 'state_name', 'total_district', 'total_school', 'total_student', 'total_teacher',
                'min_school_per_district', 'max_school_per_district', 'std_school_per_district', 'avg_school_per_district',
                'min_student_per_school', 'max_student_per_school', 'std_student_per_school', 'avg_student_per_school',
                'min_stutea_ratio_per_school', 'max_stutea_ratio_per_school', 'std_stutea_ratio_per_school', 'avg_stutea_ratio_per_school',
                'primary_perc', 'middle_perc', 'high_perc', 'other_perc']

RETRY_CAL_STAT = 50
DIST_LOW_VALUE = 0.9
DIST_HIGH_VALUE = 1.2
