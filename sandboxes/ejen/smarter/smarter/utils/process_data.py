from smarter.helpers.enums import Scope, Grain, SchoolGroupType

def get_param_info(parameters):   
    grain_info = None
    scope_info = None
    school_group_type = None
    grade_dividers_on = None
    
    if 'segment_by' in parameters.keys():
        grain_info = Grain.get_by_name(str(parameters['segment_by']))
        if grain_info != None and grain_info['inst_hierarchy_order'] == None:
            grain_info = None
    if 'report_level' in parameters.keys():
        scope_info = Scope.get_by_name(str(parameters['report_level']))
    if 'school_group_type' in parameters.keys():
        school_group_type = SchoolGroupType.get_by_name(str(parameters['school_group_type']))
    #grade_dividers_on = GradeDividers.get_by_boolean(str(parameters['grade_divider']))['boolean']
    if 'grade_divider' in parameters.keys():
        grade_dividers_on = str(parameters['grade_divider']).lower()
        if grade_dividers_on != "true" and grade_dividers_on != "false":
            grade_dividers_on = None

    #will be checked in the ui in the future
    if grain_info != None and scope_info != None and grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order']>= scope_info['inst_hierarchy_order']:
        print("level is wrong. segment_by should be lower than report_level")
        grain_info = None
        scope_info = None
    return grain_info, scope_info, school_group_type, grade_dividers_on
    
    
def get_scope_column_key(scope_code):
    scope_code_column, scope_group_key = {
        Scope.GroupOfState['code']: ('state_group_code', 'state_group'),
        Scope.State['code']: ('state_code', 'state'),
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
        Grain.GroupOfState['code']: ('state_group_code', 'state_group'),
        Grain.State['code']: ('state_code', 'state'),
        Grain.District['code']: ('school_group_code', 'school_group'),
        Grain.School['code']: ('school_code', 'school'),
        Grain.Teacher['code']: ('teacher_code', 'teacher'),
        Grain.Student['code']: ('student_code', 'student'),
        #Grain.Grade['code']: ('grade_code', 'grade'),
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
        'state_group': None if scope_info['inst_hierarchy_order'] > Scope.GroupOfState['inst_hierarchy_order'] else {
            'code': row['state_group_code'],
            'name': row['state_group_name']
         },
        'state': None if scope_info['inst_hierarchy_order'] > Scope.State['inst_hierarchy_order'] else {
            'code': row['state_code'],
            'name': row['state_name']
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
        'state_group': None if grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order'] > Grain.GroupOfState['inst_hierarchy_order'] else {
            'code': row['state_group_code'],
            'name': row['state_group_name']
         },
        'state': None if grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order'] > Grain.State['inst_hierarchy_order'] else {
            'code': row['state_code'],
            'name': row['state_name']
         },
        'school_group': None if grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order'] > Grain.District['inst_hierarchy_order'] else {
            'code': row['school_group_code'],
            'name': row['school_group_name']
         },
         'school': None if grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order'] > Grain.School['inst_hierarchy_order'] else {
             'code': row['school_code'],
             'name': row['school_name']
         },
          'teacher': None if grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order'] > Grain.Teacher['inst_hierarchy_order'] else {
              'code': row['teacher_code'],
             'name': row['teacher_name']
          },
          'student': None if grain_info['inst_hierarchy_order'] != None and grain_info['inst_hierarchy_order'] > Grain.Student['inst_hierarchy_order'] else {
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
    