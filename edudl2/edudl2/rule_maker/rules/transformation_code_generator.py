'''
Created on June 13, 2013

@author: lichen
'''
import datetime
from edudl2.rule_maker.rules.udl_transformation_config import transform_rules
from edudl2.rule_maker.rules.code_generator_special_rules import special_rules
from edudl2.rule_maker.rules.rule_keys import COMPARE_LENGTH, INLIST, OUTLIST,\
    PCLEAN, VCLEAN, LOOKUP, RCLEAN, DATE, CALCULATE
from edudl2.rule_maker.rules.code_generator_util import assignment,\
    action_fun_map, fun_name
import edudl2.rule_maker.rules.code_generator_sql_template as sql_tpl


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

    generated_rule_list = []
    for rule_name in rule_names:
        # check if it is a special rule case
        if rule_name in special_rules.keys():
            # append a tuple: rule_name, func_name, generated_sql
            generated_rule_list.append((rule_name, special_rules[rule_name][0], special_rules[rule_name][1]))
            # if this rule is also defined in rule_conf, use the one in special rule
            if rule_name in rule_conf.keys():
                print("RULE -- %s IS GENERATED AS DEFINED IN SPECIAL RULES" % rule_name)
        elif rule_name in rule_conf.keys():
            rule_def = rule_conf[rule_name]
            generated_rule_tuple = generate_single_transformation_code(code_version, rule_name, rule_def)
            # this is to exclude the rules which have not implemented yet
            if len(generated_rule_tuple[2]) > 0:
                generated_rule_list.append(generated_rule_tuple)
        else:
            print("CANNOT GENERATE CODE FOR RULE %s" % rule_name)
    return generated_rule_list


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
    code_body = generate_sql_proc_body(code_version, rule_name, action_sql_map)
    code_end = generate_sql_proc_end(code_version, rule_name, action_sql_map)
    return '\n'.join([code_top, code_body, code_end])


def generate_sql_proc_top(code_version, rule_name, action_sql_map, func_name):
    '''
    Main function to generate sql proc top part
    '''
    # initial function_basic_top includes declaration of v_col, t_col, v_result
    function_basic_top = sql_tpl.generate_func_top(code_version).format(func_name=func_name, col_name=rule_name)
    # declare array for inlist, outlist, or others if necessary
    function_extra_top = declare_arrays(code_version, rule_name, NOTATIONS, action_sql_map)
    return ''.join([function_basic_top, function_extra_top])


def declare_arrays(code_version, rule_name, notations_const, action_sql_map):
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


def generate_sql_proc_body(code_version, rule_name, action_sql_map):
    '''
    Order the action in action_sql_map, and construct the sql body
    '''
    # the basic order of the body is: BEGIN, COMMENTS, PCLEAN, VCLEAN, OTHERS
    # initialize the ordered list as the size of action_sql_map plus FOUR
    # 'FOUR' is mapping to BEGIN, COMMENTS, PCLEAN, VCLEAN
    temp_list = [''] * (len(action_sql_map) + 4)
    # add 'BEGIN' as the beginning of body
    temp_list[0] = sql_tpl.BEGIN.upper()
    temp_list[1] = generate_comments_for_proc_body(code_version, rule_name)
    # j is the index for body part which is not PCLEAN, VCLEAN and RCLEAN
    j = 4
    for key, value in action_sql_map.items():
        # if PCLEAN is available, add to index 2
        if key == PCLEAN:
            temp_list[2] = value[CODE]
        # if VCLEAN is available, add to index 3
        elif key == VCLEAN:
            temp_list[3] = value[CODE]
        # if it is other notation but not RCLEAN, add to current index j
        # RCLEAN will be handled in 'end' part
        elif key != RCLEAN:
            temp_list[j] = value[CODE]
            j += 1
    # remove useless empty item
    temp_list[:] = [i for i in temp_list if i != '']
    return '\n'.join(temp_list)


def generate_comments_for_proc_body(code_version, rule_name):
    '''
    Function to generate comments for proc body. The comments contains generated time, and code version
    '''
    # make a time comment at the beginning of each function
    time_comment = 'THIS CODE WAS GENERATED AT ' + str(datetime.datetime.now())
    comment_stat1 = sql_tpl.comment_exp[code_version].format(comment=time_comment)
    version_comment = 'THIS CODE WAS GENERATED FOR %s OF RULE %s' % (code_version.upper(), rule_name)
    comment_stat2 = sql_tpl.comment_exp[code_version].format(comment=version_comment)
    return '\n'.join([comment_stat1, comment_stat2])


def generate_sql_proc_end(code_version, rule_name, action_sql_map):
    '''
    Main function to generate sql proc ending part
    '''
    # TODO: add map for second_key
    # default ending statement
    second_key = sql_tpl.BASIC
    # if has INLIST, the ending part has the checking for 'NOT FOUND' case
    if INLIST in action_sql_map.keys():
        second_key = sql_tpl.NOT_FOUND
    # if has LOOKUP, the ending part has the if_else statement
    elif LOOKUP in action_sql_map.keys():
        second_key = sql_tpl.IF_ELSE
    # default rclean
    rclean_exp = action_sql_map[RCLEAN][CODE] if RCLEAN in action_sql_map.keys() else ''
    return sql_tpl.generate_func_end(code_version, second_key).format(col_name=rule_name,
                                                                      func_name=fun_name(tuple(FUNC_PREFIX + rule_name)),
                                                                      rclean_exp=rclean_exp)


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


__template_func_map = {DATE: generate_sql_proc_date,
                       CALCULATE: generate_sql_proc_calc}


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
