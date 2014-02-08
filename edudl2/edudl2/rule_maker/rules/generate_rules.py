'''
Created on May 29, 2013

@author: kallen
'''

from edudl2.rule_maker.makers.dataprep import __default_prep
from edudl2.rule_maker.makers.datacanon import make_function_for_look_up, make_function_for_lists
from edudl2.rule_maker.rules import rule_keys as rk


__function_map = {rk.LOOK_UP: make_function_for_look_up,
                  rk.INLIST: make_function_for_look_up,
                  rk.INLIST_COMPARE_LENGTH: make_function_for_lists,
                  rk.INLIST_WITH_OUTLIST: make_function_for_lists
                  }

rules_map = {
    # Category 1 -- look up: map accepted input to canon expression
    rk.LOOK_UP: {
        'gender': {rk.CANON: {'M': ['M', 'B'], 'F': ['F', 'G'], 'NS': ['NS', 'NOT_SPECIFIED', 'NOT SPECIFIED']}},
        'yn': {rk.CANON: {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F']}},
        'alternate': {rk.CANON: {'N': ['N'], 'MOST': ['MOST'], 'PERSIST': ['PER']}},
    },

    # Category 2 -- inlist: give a list of allowed prefix value, compare the input, then return to the matching prefix
    rk.INLIST: {
        'freeLunch': {rk.INLIST: ['N', 'RED', 'FREE', 'FR-RED']},
        'title1': {rk.INLIST: ['N', 'UN', 'READ', 'MATH', 'LANG']},
    },

    # Category 3 -- inlist with compare_length
    rk.INLIST_COMPARE_LENGTH: {
        'homeLang': {rk.INLIST: ['ARAB', 'CANT', 'FRE', 'GER', 'GRE', 'HAI', 'HEB', 'HIN', 'HMO', 'ITAL'],
                     rk.COMPARE_LENGTH: 3},
        'engProficiency': {rk.INLIST: ['NATIVE', 'FLUENT', 'LEP', 'NON', 'REDES', 'FORMER', 'HOME', 'NS'],
                           rk.LOOK_UP: {'NS': ['NOT_SPECIFIED', 'NOT SPECIFIED', 'NOTSPECIFIED']},
                           rk.COMPARE_LENGTH: 2},
    },

    # Category 4 -- inlist with outlist: give two lists as keys and values
    rk.INLIST_WITH_OUTLIST: {
        'disabSpec': {rk.INLIST: ['SPEC', 'LANG', 'SPEECH', 'EMOT', 'DISTURBANCE', 'MENT',
                                  'RETARDATION', 'HEAR', 'ORTH', 'VIS', 'AUT', 'TRAU', 'TBI',
                                  'DEV', 'DELAY', 'MUL', 'OTH', 'DEAF', 'DEAF-BLINDNESS', 'GIFT', 'NON'],
                      rk.OUTLIST: ['SPEC', 'LANG', 'LANG', 'EMOT', 'EMOT', 'MENT', 'MENT',
                                   'HEAR', 'ORTH', 'VIS', 'AUT', 'TRAU', 'TRAU', 'DEV', 'DEV',
                                   'MUL', 'OTH', 'DEAF', 'DEAF', 'GIFT', 'NON'],
                      rk.LOOK_UP: {'NON': 'N'},
                      rk.COMPARE_LENGTH: 4},
        'race': {rk.INLIST: ['an', 'alaska native', 'alaska', 'ai'],
                 rk.OUTLIST: ['AN', 'AN', 'AN', 'AI'],
                 rk.LOOK_UP: {'NS': ['not_specified']},
                 rk.COMPARE_LENGTH: 41}
    },


    # Category 5: data format
    # Category 6: value calculation
}


def generate_rules():
    '''
    Main function to generate business rules,
    including transformation rules and validation rules
    '''
    for rule_catergory, group_rules in rules_map.items():
        fun = __function_map[rule_catergory]
        for rule, parts in group_rules.items():
            # print("\n====== code for: " + rule + " ======")
            parm = parameters_with_defaults(rule_catergory, rule, parts)
            out = fun(*parm)
            print(out)


def parameters_with_defaults(rule_catergory, rule, parts):
    '''
    For different kinds of rules, this function returns
    corresponding function to generate rule and list of parts
    '''
    # rule name
    col = parts.get('col', rule)
    # do clean_up as preparation by default
    prepare = parts.get('prepare', __default_prep)
    # output parts
    output = [col, prepare]

    try:
        if rule_catergory == rk.LOOK_UP:
            canon = parts[rk.CANON]
            output.append(canon)
        elif rule_catergory == rk.INLIST:
            canon = make_canon(parts)
            output.append(canon)
        elif rule_catergory == rk.INLIST_WITH_OUTLIST:
            value_list = parts[rk.OUTLIST]
            compare_length = parts[rk.COMPARE_LENGTH]
            look_up = parts[rk.LOOK_UP]
            key_list = parts[rk.INLIST]

            output.append(value_list)
            output.append(compare_length)
            output.append(look_up)
            output.append(key_list)
        elif rule_catergory == rk.INLIST_COMPARE_LENGTH:
            value_list = parts[rk.INLIST]
            compare_length = parts[rk.COMPARE_LENGTH]

            output.append(value_list)
            output.append(compare_length)
            if rk.LOOK_UP in parts.keys():
                output.append(parts[rk.LOOK_UP])
    except:
        print("error")
    return output


def make_canon(parts):
    mylist = parts[rk.INLIST]
    canon = {}
    for ikey in mylist:
        canon[ikey] = [ikey]
    return canon


if __name__ == '__main__':
    generate_rules()
