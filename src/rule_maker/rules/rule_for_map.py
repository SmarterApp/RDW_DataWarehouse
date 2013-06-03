'''
Created on May 29, 2013

@author: kallen
'''

from rule_maker.makers.dataprep import __default_prep
from rule_maker.makers.datacanon import make_function_for_map, make_function_for_lists
from rule_maker.rules import rule_keys as rk


rules_map = {
    # Category 1: map accepted input to canon expression
    'gender': {rk.CANON: {'M': ['M', 'B'], 'F': ['F', 'G'], 'NS': ['NS', 'NOT_SPECIFIED', 'NOT SPECIFIED']}},
    'yn': {rk.CANON: {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F']}},
    'alternate': {rk.CANON: {'N': ['N'], 'MOST': ['MOST'], 'PERSIST': ['PER']}},

    # Category 2: give a list of allowed prefix value, compare the input, then return to the matching prefix
    'freeLunch': {rk.ALLOWED: ['N', 'RED', 'FREE', 'FR-RED']},
    'title1': {rk.ALLOWED: ['N', 'UN', 'READ', 'MATH', 'LANG']},

    # Category 3: give a list of returned value
    'homeLang': {rk.ONE_LIST: ['ARAB', 'CANT', 'FRE', 'GER', 'GRE', 'HAI', 'HEB', 'HIN', 'HMO', 'ITAL'],
                 rk.COMPARE_LENGTH: 3},
    'engProficiency': {rk.ONE_LIST: ['NATIVE', 'FLUENT', 'LEP', 'NON', 'REDES', 'FORMER', 'HOME', 'NS'],
                       rk.CHECK_N: {'NS': ['NOT_SPECIFIED', 'NOT SPECIFIED', 'NOTSPECIFIED']},
                       rk.COMPARE_LENGTH: 2},


    # Category 4: give two lists as keys and values
     'disabSpec': {rk.TWO_LISTS: [['SPEC', 'LANG', 'SPEECH', 'EMOT', 'DISTURBANCE', 'MENT',
                                   'RETARDATION', 'HEAR', 'ORTH', 'VIS', 'AUT', 'TRAU', 'TBI',
                                   'DEV', 'DELAY', 'MUL', 'OTH', 'DEAF', 'DEAF-BLINDNESS', 'GIFT', 'NON'],
                                  ['SPEC', 'LANG', 'LANG', 'EMOT', 'EMOT', 'MENT', 'MENT',
                                   'HEAR', 'ORTH', 'VIS', 'AUT', 'TRAU', 'TRAU', 'DEV', 'DEV',
                                   'MUL', 'OTH', 'DEAF', 'DEAF', 'GIFT', 'NON']],
                   rk.CHECK_N: {'NON': 'N'},
                   rk.COMPARE_LENGTH: 4},
     'race': {rk.TWO_LISTS: [['an', 'alaska native', 'alaska', 'ai'],
                             ['AN', 'AN', 'AN', 'AI']],
                   rk.CHECK_N: {'NS': ['not_specified']},
                   rk.COMPARE_LENGTH: 41}
    # 'access_window': {},
    # Category 5: data format
    # Category 6: value calculation
}


def generate_rules():
    '''
    Main function to generate business rules,
    including transformation rules and validation rules
    '''
    for ikey in rules_map:
        print("\n====== code for: " + ikey + " ======")
        fun, parm = parts_with_defaults(ikey)
        out = fun(*parm)
        print(out)


def parts_with_defaults(ikey):
    '''
    For different kinds of rules, this function returns
    corresponding function to generate rule and list of parameters
    '''
    parts = rules_map.get(ikey)
    col = parts.get('col', ikey)
    prepare = parts.get('prepare', __default_prep)
    parm = [col, prepare]
    fun = make_function_for_map

    if rk.CANON in parts.keys():
        canon = parts[rk.CANON]
        parm.append(canon)
    elif rk.ALLOWED in parts.keys():
        canon = make_canon(parts)
        parm.append(canon)
    elif rk.TWO_LISTS in parts.keys():
        key_list = parts[rk.TWO_LISTS][0]
        value_list = parts[rk.TWO_LISTS][1]
        check_n = parts[rk.CHECK_N]
        compare_length = parts[rk.COMPARE_LENGTH]

        parm.append(value_list)
        parm.append(compare_length)
        parm.append(check_n)
        parm.append(key_list)
        fun = make_function_for_lists
    elif rk.ONE_LIST in parts.keys():
        value_list = parts[rk.ONE_LIST]
        compare_length = parts[rk.COMPARE_LENGTH]
        parm.append(value_list)
        parm.append(compare_length)
        if rk.CHECK_N in parts.keys():
            parm.append(parts[rk.CHECK_N])
        fun = make_function_for_lists
    return fun, parm


def make_canon(parts):
    mylist = parts['allowed']
    canon = {}
    for ikey in mylist:
        canon[ikey] = [ikey]
    return canon


if __name__ == '__main__':
    generate_rules()
