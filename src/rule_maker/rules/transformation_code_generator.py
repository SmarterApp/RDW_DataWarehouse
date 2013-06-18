'''
Created on June 13, 2013

@author: lichen
'''
import datetime
from rule_maker.rules.rule_keys import PCLEAN, VCLEAN, RCLEAN, INLIST, LOOKUP, OUTLIST, COMPARE_LENGTH, DATE, CALCULATE
from rule_maker.rules.udl_transformation_config import transform_rules, CLEANERS
from rule_maker.rules.code_generator_util import action_fun_map, assignment, fun_name
import rule_maker.rules.code_generator_sql_template as sql_tpl

FUNC_PREFIX = 'sp_'
NOTATIONS = 'notations'
CODE = 'code'


def generate_transformations(rule_names, rule_conf=transform_rules, code_version=sql_tpl.POSTGRES):
    '''
    Main function to generate transformation code for given rule names
    @param rule_names  : List of rule names
    @param rule_conf   : Dictionary of rule names and rule content
                         The default value is transform_rules defined in udl_transformation_config.py
    @param code_version: Code version of procedure to be generated.
                         The default code version is postgresql.
    '''
    if code_version not in sql_tpl.SUPPORTED_VERSIONS:
        raise ValueError("DO NOT SUPPORT CODE VERSION %s" % code_version)

    generated_rule_code = []
    for rule_name in rule_names:
        if rule_name not in rule_conf.keys():
            print("CANNOT GENERATE CODE FOR RULE %s" % rule_name)
        else:
            rule_def = rule_conf[rule_name]
            generated_rule_code.append(generate_single_transformation_code(code_version, rule_name, rule_def))
    return generated_rule_code


def generate_single_transformation_code(code_version, rule_name, rule_def):
    '''
    Main function to generate one sql function for one transformation rule
    @param rule_name: rule name of the code to be generated.
                      It is a dict key in transform_rules in udl_transformation_config.py.
    @param rule_def: rule definition of the code to be generated.
                     It is a dict value in transform_rules in udl_transformation_config.py.
                     It can be described by more than one action, and for each action,
                     it can be described by more than one notations
                     Example: {PCLEAN : [UPPER, REMNL, TRIM],
                               LOOKUP : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] }
                              }
    '''
    # get extra information, for example, we need outlist and compare_length for inlist
    extra_info = get_extra_info(rule_def)
    action_sql_map = initialize_action_sql_map(rule_name, rule_def.keys())
    for action, notations in rule_def.items():
        action_sql_map[action] = {}
        action_sql_map[action][NOTATIONS] = notations
        action_sql_map[action][CODE] = generate_sql_for_action(code_version, rule_name, action, notations, extra_info)

    func_name = fun_name(tuple(FUNC_PREFIX + rule_name))
    generated_sql = generate_sql_proc(code_version, rule_name, action_sql_map, func_name)
    return (rule_name, func_name, generated_sql)


def get_extra_info(rule_def):
    '''
    Function to extract extra information for one action/notation to generate code
    For example, when INLIST is in rule_def, need to extract OUTLIST, COMPARE_LENGTH
    '''
    info = {}
    if INLIST in rule_def.keys():
        if COMPARE_LENGTH in rule_def.keys():
            info[COMPARE_LENGTH] = rule_def[COMPARE_LENGTH]
        if OUTLIST in rule_def.keys():
            info[OUTLIST] = rule_def[OUTLIST]
    return info


def initialize_action_sql_map(rule_name, key_list):
    '''
    Function to initialize the sql map
    Primarily for v_{rule_name}, and t_{rule_name}
    '''
    action_sql_map = {}
    # make default pclean expression, which assigns p_ to v_
    if PCLEAN not in key_list:
        action_sql_map[PCLEAN] = {}
        action_sql_map[PCLEAN][CODE] = assignment('v_{col_name}', 'p_{col_name}', col_name=rule_name)
    # make default vclean expression, which assigns v_ to t_
    if VCLEAN not in key_list:
        action_sql_map[VCLEAN] = {}
        action_sql_map[VCLEAN][CODE] = assignment('t_{col_name}', 'v_{col_name}', col_name=rule_name)
    return action_sql_map


def generate_sql_for_action(code_version, rule_name, action, notations, extra_info):
    '''
    Main function to generate part of postgresql code for a given action
    @param code_version: code version of procedure to be generated
    @param rule_name: rule name of the code to be generated
    @param action: one action of the code to be generated. e.g. PCLEAN, VCLEAN, etc
    @param notatoins: notations for current action
    @param extra_info: a dictionary which has extra information to generate code for given action
    Example:
    rule_name: clean
    action: PCLEAN
    notations: [UPPER, REMNL, TRIM]
    extra_info: {}
    output:  v_yn = TRIM(REPLACE(UPPER(p_yn), CHR(13), NULL));
    '''
    if action in action_fun_map.keys():
        # if the action is inlist, we need to know the outlist, and compare_length
        parm = extra_info if action is INLIST else {}
        return action_fun_map[action](code_version, rule_name, notations, **parm)
    else:
        # temporary solution. Can be decided when writing code for rules: DATE and CALCULATION
        print("This is not available now...%s, %s", rule_name, action)
        return ''


def generate_sql_proc(code_version, rule_name, action_sql_map, func_name):
    '''
    Main function to generate complete procedure code of one function
    @param code_version: code version of procedure to be generated
    @param rule_name: rule name of the code to be generated
    @param action_sql_map: a dictionary which has generated procedure code
                           for small pieces
    '''
    # set default function
    func = generate_sql_proc_default
    # find the correct sql generator template
    for notation in list(__template_func_map.keys()):
        if notation in action_sql_map:
            func = __template_func_map[notation]
            break
    return func(code_version, rule_name, action_sql_map, func_name)


def generate_sql_proc_default(code_version, rule_name, action_sql_map, func_name):
    '''
    Main function to generate complete sql code of one function for LOOKUP, INLIST, OUTLIST
    @param code_version: code version of procedure to be generated
    @param rule_name: rule name of the code to be generated
    @param action_sql_map: a dictionary which has generated procedure code
                           for small pieces
    '''
    # get code top, body and end separately, then combine them together
    code_top = generate_sql_proc_top(code_version, rule_name, action_sql_map, func_name)
    code_body = generate_sql_proc_body(action_sql_map)
    code_end = generate_sql_proc_end(code_version, rule_name, action_sql_map.keys())
    return '\n'.join([code_top, code_body, code_end])


def generate_sql_proc_top(code_version, rule_name, action_sql_map, func_name):
    '''
    Main function to generate sql proc top part
    '''
    # make a time comment at the beginning of each function
    time_comment = 'GENERATED AT ' + str(datetime.datetime.now()) + '\n'
    comment_stat = sql_tpl.comment_exp[code_version].format(comment=time_comment)
    # initial function_basic_top includes declaration of v_col, t_col, v_result
    function_basic_top = sql_tpl.generate_func_top(code_version, comment_stat).format(func_name=func_name, col_name=rule_name)
    # declare array for inlist, outlist, or others if necessary
    function_extra_top = declare_arraies(code_version, rule_name, NOTATIONS, action_sql_map)
    return ''.join([function_basic_top, function_extra_top])


def declare_arraies(code_version, rule_name, notations_const, action_sql_map):
    '''
    Function to generate array declaration expression for inlist or outlist
    '''
    declare_array = []
    if INLIST in action_sql_map.keys():
        if OUTLIST in action_sql_map.keys():
            declare_array.append(sql_tpl.array_exp[code_version].format(prefix='keys_', col_name=rule_name, value_list="\',\'".join(action_sql_map[INLIST][notations_const])))
            declare_array.append(sql_tpl.array_exp[code_version].format(prefix='vals_', col_name=rule_name, value_list="\',\'".join(action_sql_map[OUTLIST][notations_const])))
        else:
            declare_array.append(sql_tpl.array_exp[code_version].format(prefix='vals_', col_name=rule_name, value_list="\',\'".join(action_sql_map[INLIST][notations_const])))

    # may add more code for new cases
    return '\n'.join(declare_array)


def generate_sql_proc_body(action_sql_map):
    '''
    Order the action in action_sql_map, and construct the sql body
    '''
    # the basic order of the body is: PCLEAN, VCLEAN, OTHERS, RCLEAN
    # initialize the ordered list as the size of action_sql_map plus three
    # 'Three' is mapping to PCLEAN, VCLEAN and RCLEAN
    temp_list = ['' for _i in range(len(action_sql_map) + len(CLEANERS))]
    # j is the index for body part which is not PCLEAN, VCLEAN and RCLEAN
    j = 2
    for key, value in action_sql_map.items():
        # if PCLEAN is available, add to index 0
        if key == PCLEAN:
            temp_list[0] = value[CODE]
        # if VCLEAN is available, add to index 1
        elif key == VCLEAN:
            temp_list[1] = value[CODE]
        # if RCLEAN is available, add to index -1, end of body
        elif key == RCLEAN:
            temp_list[-1] = value[CODE]
        # if it is other notation, add to current index j
        else:
            temp_list[j] = value[CODE]
            j += 1
    # remove useless empty item
    temp_list[:] = [i for i in temp_list if i != '']
    # add 'BEGIN' as the beginning of body
    temp_list.insert(0, sql_tpl.BEGIN.upper())
    return '\n'.join(list(temp_list))


def generate_sql_proc_end(code_version, rule_name, key_list):
    '''
    Main function to generate sql proc ending part
    '''
    # default ending statement
    second_key = sql_tpl.BASIC
    # if has INLIST, the ending part has the checking for 'NOT FOUND' case
    if INLIST in key_list:
        second_key = sql_tpl.NOT_FOUND
    # if has LOOKUP, the ending part has the if_else statement
    elif LOOKUP in key_list:
        second_key = sql_tpl.IF_ELSE
    return  sql_tpl.generate_func_end(code_version, second_key).format(col_name=rule_name,
                                                                       func_name=fun_name(tuple(FUNC_PREFIX + rule_name)))


def generate_sql_proc_date(code_version, rule_name, action_sql_map, func_name):
    '''
    Main function to generate complete sql code of one function for DATE format
    '''
    # TODO:
    # return 'date rule template for %s' % str(action_sql_map)
    return ''


def generate_sql_proc_calc(code_version, rule_name, action_sql_map, func_name):
    '''
    Main function to generate complete sql code of one function for CALCULATION
    '''
    # TODO:
    # return 'calc rule template for %s' % str(action_sql_map)
    return ''


__template_func_map = {
                       DATE: generate_sql_proc_date,
                       CALCULATE: generate_sql_proc_calc
                       }


if __name__ == '__main__':
    rule_names = transform_rules.keys()
    rule_conf = transform_rules
    trans_code_list = generate_transformations(rule_names, rule_conf=rule_conf)
    for rule_pair in trans_code_list:
        # print('********************')
        # print('RULE NAME -- %s' % rule_pair[0])
        # print('PROC NAME -- \n%s' % rule_pair[1])
        # print('PROC CODE -- \n%s' % rule_pair[2])
        print(rule_pair[2])
