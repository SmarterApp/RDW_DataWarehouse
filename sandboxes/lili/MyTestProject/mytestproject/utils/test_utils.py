    
def make_data(values):
    key_list = ['student_key',
                'student_code',
                'student_name',
                'assessment_score',
                'student_count', 
                'teacher_code', 
                'teacher_name',
                'school_code', 
                'school_name', 
                'school_group_code', 
                'school_group_name', 
                'time_id', 
                'grade_order', 
                'grade_name', 
                'subject_name',
                'period_name', 
                'year_range', 
                'state_group_name',
                'state_group_code', 
                'state_name',
                'state_code',
                'performance_level'
                    ]
    data = []
    for value in values:
        data.append(dict(zip(key_list, value)))
    #print(data)
    return data