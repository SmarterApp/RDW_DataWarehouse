'''
Created on June 13, 2013

@author: lichen
'''

import rule_maker.rules.udl_transformation_config as tr


def generate_transformation_rules():
    '''
    Main function to generate all transformation rules defined in udl_transformation_config.py
    '''
    trans_rules_generated = []
    for _rule_name, rule_def in tr.transform_rules.items():
        trans_rules_generated.append(generate_single_transformation_rule(rule_def))
    return rule_def


def generate_single_transformation_rule(rule_def):
    '''
    Main function to generate one transformation rule
    The rule definition is passed in, and it might be described by more than one notations
    Example:  { PCLEAN  : [UPPER, REMNL, TRIM],
                LOOKUP  : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] }
              }
    '''
    pass


if __name__ == '__main__':
    generate_transformation_rules()
