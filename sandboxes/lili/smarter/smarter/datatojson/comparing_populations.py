# from sqlalchemy import create_engine
from smarter.helpers import add_percentage_to_bar
from smarter.utils.process_data import get_param_info, get_scope_column_key, get_grain_column_key, \
                                                build_scope_group, build_grade_group, build_bar_group, build_bar, build_bar_segment
    
def comparing_populations(parameters, filtered_rows):

    """
    Main function for the Comparing Populations report service. Returns a dictionary
    with the report data.
    """
    grain_info, scope_info, school_group_type, grade_dividers_on = get_param_info(parameters)
        
    if grain_info is None or scope_info is None or school_group_type is None or grade_dividers_on is None:
        return "Input is wrong, please try it again"
        
    scope_code_column, scope_group_key = get_scope_column_key(scope_info['code'])
    grain_code_column, bar_group_key = get_grain_column_key(grain_info['code'])

    #return
    
    # Turn rows into data dict
    data = {
         'scope_groups': [],
         }
        
    current_scope_group = None
    current_grade_group = None        
    current_bar_group = None
    current_bar = None
        
    # create json
    for row in filtered_rows:
        print(row)
    
        # level 1: 'report_level'
        need_new_scope_group = current_scope_group is None or \
            (scope_code_column is not None and row[scope_code_column] != current_scope_group[scope_group_key]['code'])
        if need_new_scope_group:
            current_grade_group = None
            current_bar_group = None
            current_bar = None
            current_scope_group = build_scope_group(parameters['school_group_type'], row, school_group_type, scope_info)
            data['scope_groups'].append(current_scope_group)
            
        # level 2: 'grade_dividers'
        need_new_grade_group = current_grade_group is None or \
            (grade_dividers_on and row['grade_order'] != current_grade_group['grade']['code'])
        if need_new_grade_group:
            current_bar_group = None
            current_bar = None
            current_grade_group = build_grade_group(grade_dividers_on, row['grade_order'], row['grade_name'])
            current_scope_group['grade_groups'].append(current_grade_group)
            
        # level 3: 'segment_by'
        need_new_bar_group = current_bar_group is None or \
            (grain_code_column is not None and row[grain_code_column] != current_bar_group[bar_group_key]['code'])
        if need_new_bar_group:
            current_bar = None
            current_bar_group = build_bar_group(grain_info, row)
            current_grade_group['bar_groups'].append(current_bar_group)
    
        # level 4 of each bar
        need_new_bar = current_bar is None or \
            row['period_name'] != current_bar['period']['name'] or row['year_range'] != current_bar['year']['name']
        if need_new_bar:
            current_bar = build_bar(row['year_range'], row['period_name'])
            current_bar_group['bars'].append(current_bar)
            
        # level 5 of segment in a bar
        bar_segment = build_bar_segment(row)
        current_bar['segments'].append(bar_segment)
        current_bar['student_count'] += row['student_count']
    
    # Fill out percentages
    for scope_group in data['scope_groups']:
        for grade_group in scope_group['grade_groups']:
            for bar_group in grade_group['bar_groups']:
                for bar in bar_group['bars']:
                    add_percentage_to_bar(bar)
    # close db connection
    # db_connection.close()
    return data
