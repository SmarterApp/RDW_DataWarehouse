BIRDS_FILE = "../datafiles/birds.txt"
MANMALS_FILE = "../datafiles/manmals.txt"
FISH_FILE = "../datafiles/fish.txt"
SCHOOL_LEVELS_INFO = [
                    ['Primary', ['EL SCH', 'ELEM', 'CTR', 'ELEMENTARY SCHOOL', 'CHILDHOOD CENTER', 'PRIMARY', 'ELEMENTARY', 'CETR, ELEM', 'SCH'], [[0, 5], [1, 5], [1, 6]]],
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

ASSMT_TYPES = {'Math':{
                       '4':{ 
                             'claim_names': ['Number properties and operations', 'Measurement and Geometry', 'Data analysis, statistics, and probability', 'Algebra'],
                             'claim_percs': [40, 35, 10, 15]
                             },
                        '8':{
                             'claim_names': ['Number properties and operations', 'Measurement and Geometry', 'Data analysis, statistics, and probability', 'Algebra'],
                             'claim_percs': [20, 35, 15, 30]
                             }
                        
                        },
               'ELA':{
                       '4':{ 
                             'claim_names': ['Literary text and Fiction', 'Literary nonfiction and Poetry', 'Informational text and Exposition', 'Argumentation and persuasive text'],
                             'claim_percs': [25, 25, 25, 25]
                             },
                        '8':{
                             'claim_names': ['Literary text and Fiction', 'Literary nonfiction and Poetry', 'Informational text and Exposition', 'Argumentation and persuasive text'],
                             'claim_percs': [20, 25, 25, 30]
                             }
                        }
                }


# Output files for use in write_to_csv.py and generate data.py
STATES = '../datafiles/states.csv'
DISTRICTS = '../datafiles/districts.csv'
SCHOOLS = '../datafiles/schools.csv'
PARENTS = '../datafiles/parents.csv'
ASSESSMENT_TYPES = '../datafiles/assessment_types.csv'
STUDENT_SECTIONS = '../datafiles/stu_sections.csv'
TEACHER_SECTIONS = '../datafiles/tea_sections.csv'

ENT_LIST = [STATES, DISTRICTS, SCHOOLS, PARENTS, ASSESSMENT_TYPES, STUDENT_SECTIONS, TEACHER_SECTIONS]