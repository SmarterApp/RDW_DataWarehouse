birds_file = "../datafiles/birds.txt"
manmals_file = "../datafiles/manmals.txt"
fish_file = "../datafiles/fish.txt"
school_levels_info = [
                    ['Primary', ['EL SCH', 'ELEM', 'CTR', 'ELEMENTARY SCHOOL', 'CHILDHOOD CENTER', 'PRIMARY', 'ELEMENTARY', 'CETR, ELEM', 'SCH'], [[0, 5], [1, 5], [1, 6]]],
                    ['Middle', ['MIDDLE SCHOOL', 'COMMUNITY MIDDLE', 'MIDDLE', 'JUNIOR HIGH', 'INTERMEDIATE SCHOOL', 'JR MIDDLE', 'MS'], [[6, 8], [5, 8], [7, 9]]],
                    ['High', ['HIGH SCH', 'HIGH SCHOOL', 'HIGH', 'HS', 'SENIOR HIGH'], [[9, 12], [10, 12]]],
                    ['Other', ['SCH', 'SCHOOL'], [[6, 12], [9, 12]]]
                    ]

dist_suffix = ['DISTRICT', 'SCHOOL DISTRICT', 'SCHOOLS', 'COUNTY SCHOOLS', 'PUBLIC SHCOOLS', 'SD']
add_suffix = ["ROAD", "AVE", "STREET", "SOUTH AVE", "NORTH AVE", "WAY"]

subjects = ["Math", "ELA"]
min_class_size = 20
min_section_size = 10
gender_ratio = [0.5, 0.45, 0.55]

min_score = 50
max_score = 500
asmt_types = {'Math':[
                       {'4':[{'Number properties and operations': 40}, {'Measurement and Geometry': 35}, {'Data analysis, statistics, and probability': 10}, {'Algebra': 15}]},
                       {'8':[{'Number properties and operations': 20}, {'Measurement and Geometry': 35}, {'Data analysis, statistics, and probability': 15}, {'Algebra': 30}]}
                     ],
              'ELA':[
                       {'4':[{'Number properties and operations': 40}, {'Measurement and Geometry': 35}, {'Data analysis, statistics, and probability': 10}, {'Algebra': 15}]},
                       {'8':[{'Number properties and operations': 20}, {'Measurement and Geometry': 35}, {'Data analysis, statistics, and probability': 15}, {'Algebra': 30}]}
                     ],
               }
              
