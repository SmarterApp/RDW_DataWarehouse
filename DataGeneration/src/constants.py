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
ASSMT_TYPES = {'Math':[
                       {'4':[{'Number properties and operations': 40}, {'Measurement and Geometry': 35}, {'Data analysis, statistics, and probability': 10}, {'Algebra': 15}]},
                       {'8':[{'Number properties and operations': 20}, {'Measurement and Geometry': 35}, {'Data analysis, statistics, and probability': 15}, {'Algebra': 30}]}
                     ],
              'ELA':[
                     {'4':[{'Literary text and Fiction': 25}, {'Literary nonfiction and Poetry': 25}, {'Informational text and Exposition': 25}, {'Argumentation and persuasive text': 25}]},
                     {'8':[{'Literary text and Fiction': 20}, {'Literary nonfiction and Poetry': 25}, {'Informational text and Exposition': 25}, {'Argumentation and persuasive text': 30}]}
                     ],
               }
