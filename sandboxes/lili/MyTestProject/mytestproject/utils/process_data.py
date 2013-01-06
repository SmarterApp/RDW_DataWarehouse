from mytestproject.helpers.enums import Scope, Grain, SchoolGroupType

def get_param_info(parameters):
    #print(parameters)
    
    grain_info = None
    scope_info = None
    school_group_type = None
    
    grain_info = Grain.get_by_name(str(parameters['segment_by']))
    scope_info = Scope.get_by_name(str(parameters['report_level']))
    school_group_type = SchoolGroupType.get_by_name(str(parameters['school_group_type']))
    #grade_dividers_on = GradeDividers.get_by_boolean(str(parameters['grade_divider']))['boolean']
    grade_dividers_on = str(parameters['grade_divider']).lower()
    if grade_dividers_on != "true" and grade_dividers_on != "false":
        grade_dividers_on = None
    return grain_info, scope_info, school_group_type, grade_dividers_on
    
    
def get_scope_column_key(scope_code):    
    scope_code_column, scope_group_key = {
        #Scope.Account['code']: (None, None),
        Scope.District['code']: ('school_group_code', 'school_group'),
        #Scope.Program['code']: ('school_group_code', 'school_group'),
        Scope.School['code']: ('school_code', 'school'),
        Scope.Teacher['code']: ('teacher_code', 'teacher'),
        #Scope.Section['code']: ('section_code', 'section')
    }[scope_code]
    
    print('report level ==> scope_code_column' + " ==> " + scope_code_column + " : " + scope_group_key)    
    return scope_code_column, scope_group_key


def get_grain_column_key(grain_code):
    grain_code_column, bar_group_key = {
        #Grain.Account['code']: (None, None),
        Grain.District['code']: ('school_group_code', 'school_group'),
        #Grain.Program['code']: ('school_group_code', 'school_group'),
        Grain.School['code']: ('school_code', 'school'),
        Grain.Teacher['code']: ('teacher_code', 'teacher'),
        Grain.Student['code']: ('student_code', 'student'),
        Grain.Grade['code']: ('grade_code', 'grade'),
    }[grain_code]
    
    print('segment result by ==> grain_code_column' + " ==> " + grain_code_column + " : " + bar_group_key)
    return grain_code_column, bar_group_key

def build_scope_group(param_school_group_type, row, school_group_type, scope_info):        
    current_scope_group = {
        'grade_groups': [],
        'school_group_type': {
            'code': school_group_type['code'] if param_school_group_type != 'Not Applicable' else None,
            'name': school_group_type['name'] if param_school_group_type != 'Not Applicable' else None
         },
        'school_group': None if scope_info['inst_hierarchy_order'] > Scope.District['inst_hierarchy_order'] else {
            'code': row['school_group_code'],
            'name': row['school_group_name']
         },
        'school': None if scope_info['inst_hierarchy_order'] > Scope.School['inst_hierarchy_order'] else {
            'code': row['school_code'],
             'name': row['school_name']
         },
        'teacher': None if scope_info['inst_hierarchy_order'] > Scope.Teacher['inst_hierarchy_order'] else {
             'code': row['teacher_code'],
            'name': row['teacher_name']
        }
    }
    return current_scope_group

def build_grade_group(grade_dividers_on, grade_code, grade_name):
    current_grade_group = {
        'bar_groups': [],
        'grade': None if not grade_dividers_on else {
            'code': grade_code,
            'name': grade_name
        }
    }
    return current_grade_group


def build_bar_group(grain_info, row):
    current_bar_group = {
        'bars': [],
        'school_group': None if grain_info['inst_hierarchy_order'] > Grain.District['inst_hierarchy_order'] else {
            'code': row['school_group_code'],
            'name': row['school_group_name']
         },
         'school': None if grain_info['inst_hierarchy_order'] > Grain.School['inst_hierarchy_order'] else {
             'code': row['school_code'],
             'name': row['school_name']
         },
          'teacher': None if grain_info['inst_hierarchy_order'] > Grain.Teacher['inst_hierarchy_order'] else {
              'code': row['teacher_code'],
             'name': row['teacher_name']
          },
          'student': None if grain_info['inst_hierarchy_order'] > Grain.Student['inst_hierarchy_order'] else {
              'code': row['student_code'],
              'name': row['student_name'],
               #'student_sid': row['student_sid'],
         },
         'grade': None if grain_info != Grain.Grade else {
            'code': row['grade_order'],
            'name': row['grade_name']
        }
    }
    return current_bar_group

def build_bar(year_name, period_name):
    current_bar = {
        'segments': [],
        'student_count': 0,
        'year': {
            'code': None, #row['year_code'],
            'name': year_name
        },
        'period': {
            'code': None, #row['period_code'],
            'name': period_name
        }
    }
    return current_bar


def build_bar_segment(row):
    bar_segment = {
            'performance_level': None if row['performance_level'] is None else
            {
                'code': row['performance_level'],
                'name': row['performance_level']
            },
            'student_count': row['student_count'],
            'student_percentage': None,  # Filled in later
            'score': int(round(row['assessment_score']))
        }
    return bar_segment
    