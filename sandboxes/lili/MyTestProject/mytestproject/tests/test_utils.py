    
def make_data(values):
    key_list = ['student_key',
                'student_code',
                'student_name',
                'score',
                'student_code',
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
                'year_name', 
                'state_group_name', 
                'state_name', 
                'perf_level_name', 
                'perf_level_code'
                    ]
    data = []
    for value in values:
        data.append(dict(zip(key_list, value)))
    print(data)
    return data