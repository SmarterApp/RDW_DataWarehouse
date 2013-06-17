'''
Created on June 13, 2013

@author: lichen
'''
from rule_maker.rules.rule_keys import PCLEAN, VCLEAN, RCLEAN, INLIST, LOOKUP, OUTLIST, COMPARE_LENGTH, DATE, CALCULATE
from rule_maker.rules.udl_transformation_config import transform_rules, CLEANERS
from rule_maker.rules.code_generator_util import action_fun_map, assignment, array_exp, declare_arraies
import rule_maker.rules.code_generator_sql_template as sql_tpl

FUNC_PREFIX = 'sp_'
NOTATIONS = 'notations'
CODE = 'code'


def generate_transformations(code_version=sql_tpl.POSTGRES):
    '''
    Main function to generate all transformation
    rules defined in udl_transformation_config.py.
    The default code version is postgresql.
    '''
    if code_version not in sql_tpl.SUPPORTED_VERSIONS:
        print("Do not support version %s" % code_version)
        raise Exception

    generated_code = []
    for rule_name, rule_def in transform_rules.items():
        generated_code.append(generate_single_transformation_code(code_version, rule_name, rule_def))

    return generated_code


def generate_single_transformation_code(code_version, rule_name, rule_def):
    '''
    Main function to generate one transformation rule
    The rule definition is passed in, and it might be described by more than one notations
    Example:  { PCLEAN  : [UPPER, REMNL, TRIM],
                LOOKUP  : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] }
              }
    '''
    # get extra information, for example, we need outlist and compare_length information for inlist
    extra_info = get_extra_info(rule_def)
    action_sql_map = {}
    for action, notations in rule_def.items():
        action_sql_map[action] = {}
        action_sql_map[action][NOTATIONS] = notations
        action_sql_map[action][CODE] = generate_sql_for_action(code_version, rule_name, action, notations, extra_info)

    # make default vclean expression, which assigns v_ to t_
    if VCLEAN not in rule_def.keys():
        action_sql_map[VCLEAN] = {}
        action_sql_map[VCLEAN][CODE] = assignment('t_{col_name}', 'v_{col_name}', col_name=rule_name)
    return generate_sql_proc(code_version, rule_name, action_sql_map)


def get_extra_info(rule_def):
    info = {}
    if INLIST in rule_def.keys():
        if COMPARE_LENGTH in rule_def.keys():
            info[COMPARE_LENGTH] = rule_def[COMPARE_LENGTH]
        if OUTLIST in rule_def.keys():
            info[OUTLIST] = rule_def[OUTLIST]
    return info


def generate_sql_for_action(code_version, rule_name, action, notations, extra_info):
    '''
    Main function to generate part of postgresql code for the given action
    Example:
    input:   {PCLEAN: [UPPER, REMNL, TRIM]}
    output:  v_yn = TRIM(REPLACE(UPPER(p_yn), CHR(13), NULL));
    '''
    if action in action_fun_map.keys():
        parm = {}
        # if the action is inlist, we need to know the outlist, and compare_length
        if action is INLIST:
            if COMPARE_LENGTH in extra_info.keys():
                parm[COMPARE_LENGTH] = extra_info[COMPARE_LENGTH]
            if OUTLIST in extra_info.keys():
                parm[OUTLIST] = extra_info[OUTLIST]
        return action_fun_map[action](code_version, rule_name, notations, **parm)
    else:
        # temporary
        return ''


def generate_sql_proc(code_version, rule_name, action_sql_map):
    '''
    Main function to generate complete sql code of one function
    '''
    func = generate_sql_proc_default
    # find the correct sql generator template
    for notation in list(__template_func_map.keys()):
        if notation in action_sql_map:
            func = __template_func_map[notation]
            break
    return func(code_version, rule_name, action_sql_map)


def generate_sql_proc_default(code_version, rule_name, action_sql_map):
    '''
    Main function to generate complete sql code of one function for LOOKUP, INLIST, OUTLIST
    '''
    code_top = generate_sql_proc_top(code_version, rule_name, action_sql_map)
    code_body = generate_sql_proc_body(action_sql_map)
    code_end = generate_sql_proc_end(code_version, rule_name, action_sql_map)
    return '\n'.join([code_top, code_body, code_end])


def generate_sql_proc_top(code_version, rule_name, action_sql_map):
    '''
    Main function to generate sql proc top part
    '''
    # initial function_basic_top includes declaration of v_col, t_col, v_result
    function_basic_top = sql_tpl.generate_func_top(code_version).format(func_name=FUNC_PREFIX + rule_name, col_name=rule_name)
    # check if need to declare array for inlist, outlist, or others
    return ''.join([function_basic_top, declare_arraies(code_version, rule_name, NOTATIONS, action_sql_map)])


def generate_sql_proc_body(action_sql_map):
    '''
    Order the action in action_sql_map, and construct the sql body
    '''
    temp_list = ['' for _i in range(len(action_sql_map) + 3)]
    j = 2
    for key, value in action_sql_map.items():
        if key == PCLEAN:
            temp_list[0] = value[CODE]
        elif key == VCLEAN:
            temp_list[1] = value[CODE]
        elif key == RCLEAN:
            temp_list[-1] = value[CODE]
        else:
            temp_list[j] = value[CODE]
            j += 1
    temp_list[:] = [i for i in temp_list if i != '']
    temp_list.insert(0, sql_tpl.BEGIN.upper())
    return '\n'.join(list(temp_list))


def generate_sql_proc_end(code_version, rule_name, action_sql_map):
    '''
    Main function to generate sql proc ending part
    '''
    second_key = sql_tpl.BASIC
    if INLIST in action_sql_map.keys():
        second_key = sql_tpl.NOT_FOUND
    elif LOOKUP in action_sql_map.keys():
        second_key = sql_tpl.IF_ELSE
    return  sql_tpl.generate_func_end(code_version, second_key).format(col_name=rule_name, func_name=FUNC_PREFIX + rule_name)


def generate_sql_proc_date(code_version, rule_name, action_sql_map):
    '''
    Main function to generate complete sql code of one function for DATE format
    '''
    # TODO:
    return 'date rule template for %s' % str(action_sql_map)


def generate_sql_proc_calc(code_version, rule_name, action_sql_map):
    '''
    Main function to generate complete sql code of one function for CALCULATION
    '''
    # TODO:
    return 'calc rule template for %s' % str(action_sql_map)


__template_func_map = {
                       DATE: generate_sql_proc_date,
                       CALCULATE: generate_sql_proc_calc
                       }


if __name__ == '__main__':
    trans_code_list = generate_transformations()
    for rule in trans_code_list:
        print(rule)
