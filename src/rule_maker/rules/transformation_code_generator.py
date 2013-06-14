'''
Created on June 13, 2013

@author: lichen
'''
from rule_maker.rules.rule_keys import PCLEAN, VCLEAN, RCLEAN, DATE, CALCULATE
from rule_maker.rules.udl_transformation_config import transform_rules, CLEANERS
from rule_maker.rules.code_generator_util import action_fun_map
import rule_maker.rules.code_generator_sql_template as sql_tpl

FUNC_PREFIX = 'sp_'


def generate_transformations():
    '''
    Main function to generate all transformation
    rules defined in udl_transformation_config.py
    '''
    generated_code = []
    for rule_name, rule_def in transform_rules.items():
        generated_code.append(generate_single_transformation_code(rule_name, rule_def))

    return generated_code


def generate_single_transformation_code(rule_name, rule_def):
    '''
    Main function to generate one transformation rule
    The rule definition is passed in, and it might be described by more than one notations
    Example:  { PCLEAN  : [UPPER, REMNL, TRIM],
                LOOKUP  : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] }
              }
    '''
    action_sql_map = {}
    for action, notations in rule_def.items():
        action_sql_map[action] = generate_sql_for_notation(rule_name, action, notations)

    if VCLEAN not in rule_def.keys():
        action_sql_map[VCLEAN] = generate_assignment_sql('t_{col_name}', 'v_{col_name}', {'col_name': rule_name})
    return generate_sql_proc(rule_name, action_sql_map)


def generate_sql_for_notation(rule_name, action, notations):
    '''
    Main function to generate part of postgresql code for the given action
    Example:
    input:   {PCLEAN: [UPPER, REMNL, TRIM]}
    output:  v_yn = TRIM(REPLACE(UPPER(p_yn), CHR(13), NULL));
    '''
    if action in action_fun_map.keys():
        # result = action_fun_map[action](rule_name, notations)
        return action_fun_map[action](rule_name, notations)
    else:
        return '\t\tPOSTGRESQL code for %s, %s\n' % (str(action), str(notations))


def generate_assignment_sql(left_exp, right_exp, parm):
    return ''.join([left_exp, ' := ', right_exp]).format(**parm)
    # 't_{col_name} := v_{col_name}'.format(col_name=rule_name)


def generate_sql_proc(rule_name, action_sql_map):
    '''
    Main function to generate complete postgresql code of one function
    '''
    func = generate_sql_proc_default
    # find the correct sql generator template
    for notation in list(__template_func_map.keys()):
        if notation in action_sql_map:
            func = __template_func_map[notation]
            break
    return func(rule_name, action_sql_map)


def generate_sql_proc_default(rule_name, action_sql_map):
    has_body_except_for_clean = len(set(action_sql_map.keys()) - CLEANERS) > 0
    code_top = sql_tpl.func_top.format(func_name=FUNC_PREFIX + rule_name, col_name=rule_name)
    code_body = generate_sql_proc_body(action_sql_map)
    code_end = (sql_tpl.func_end if has_body_except_for_clean else sql_tpl.func_end_basic).format(col_name=rule_name)
    return '\n'.join([code_top, code_body, code_end])


def generate_sql_proc_body(action_sql_map):
    '''
    Order the action in action_sql_map, and construct the sql body
    '''
    temp_list = ['' for _i in range(len(action_sql_map))]
    j = 2
    for key, value in action_sql_map.items():
        if key == PCLEAN:
            temp_list[0] = value
        elif key == VCLEAN:
            temp_list[1] = value
        elif key == RCLEAN:
            temp_list[-1] = value
        else:
            temp_list[j] = value
            j += 1
    return '\n'.join(list(temp_list))


def generate_sql_proc_date(rule_name, action_sql_map):
    # TODO:
    return 'date rule template for %s' % str(action_sql_map)


def generate_sql_proc_calc(rule_name, action_sql_map):
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
