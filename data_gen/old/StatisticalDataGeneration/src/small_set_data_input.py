
# number of school in each of district. Length of this list presents number of districts
SMALL_SET_SCHOOL_NUM_IN_DIST = [3, 3]

# number of student in each of the school. Length of this list presents number of schools
SMALL_SET_STUDENT_NUM_IN_SCHOOL = [35, 5, 11, 4, 20, 6]

# student_teacher_ratio in each of the school. Length of this list presents number of schools
SMALL_SET_STUDENT_TEACHER_RATIO_IN_SCHOOL = [8.75, 5, 5.5, 4, 6.67, 3]

# school type of each school. Length of this list presents number of schools
SMALL_SET_SCHOOL_TYPE_IN_STATE = ['Elementary School', 'Middle School', 'High School', 'Elementary School', 'Middle School', 'High School']

# number of school-staff in school
SMALL_SET_SCHOOL_STAFF_NUM_IN_SCHOOL = 1

# dictionary of low, high grade of each type of school.
# Key is the school type, value is a tuple. First value in tuple is the low grade, and second value in tuple is the high grade
SMALL_SET_SCHOOL_TYPE_GRADES = {'Elementary School': (3, 3),
                                'Middle School': (8, 8),
                                'High School': (11, 11)
                                }

# Notes:
# 1. length of SMALL_SET_STUDENT_NUM_IN_SCHOOL, SMALL_SET_STUDENT_TEACHER_RATIO_IN_SCHOOL and SMALL_SET_SCHOOL_TYPE_IN_STATE equals to sum(SMALL_SET_SCHOOL_NUM_IN_DIST)
# 2. In SMALL_SET_SCHOOL_TYPE_GRADES, for each tuple in values(), first value should be less than the second value. Both two values should in range(0, 13)
