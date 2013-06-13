'''
Created on June 13, 2013

@author: lichen
'''
from rule_maker.rules.rule_keys import PCLEAN, VCLEAN, DATE, CALCULATE
from rule_maker.rules.udl_transformation_config import transform_rules


def generate_transformation_rules():
    '''
    Main function to generate all transformation
    rules defined in udl_transformation_config.py
    '''
    trans_rules_generated = []
    for _rule_name, rule_def in transform_rules.items():
        trans_rules_generated.append(generate_single_transformation_rule(rule_def))

    return trans_rules_generated


def generate_single_transformation_rule(rule_def):
    '''
    Main function to generate one transformation rule
    The rule definition is passed in, and it might be described by more than one notations
    Example:  { PCLEAN  : [UPPER, REMNL, TRIM],
                LOOKUP  : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] }
              }
    '''
    action_sql_map = {}
    for action, notations in rule_def.items():
        action_sql_map[action] = generate_sql_for_notation(action, notations)

    return generate_sql_proc(action_sql_map)


def generate_sql_for_notation(action, notations):
    '''
    Main function to generate part of postgresql code for the given action
    Example:
    input:   {PCLEAN: [UPPER, REMNL, TRIM]}
    output:  v_yn = TRIM(REPLACE(UPPER(p_yn), CHR(13), NULL));
    '''
    pass


def generate_sql_proc(action_sql_map):
    '''
    Main function to generate complete postgresql code of one function
    '''
    func = generate_sql_proc_default
    # find the correct sql generator template
    for notation in list(__template_func_map.keys()):
        if notation in action_sql_map:
            func = __template_func_map[notation]
            break
    return func()


def generate_sql_proc_default():
    pass


def generate_sql_proc_date():
    pass


def generate_sql_proc_calc():
    pass


__template_func_map = {DATE: generate_sql_proc_date,
                       CALCULATE: generate_sql_proc_calc
                       }


if __name__ == '__main__':
    generate_transformation_rules()
