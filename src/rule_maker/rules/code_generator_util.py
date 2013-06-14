'''
Created on June 13, 2013

@author: lichen
'''
from rule_maker.rules.rule_keys import PCLEAN, VCLEAN, LOOKUP, DATE, CALCULATE


def lower(col_name):
    return 'LOWER(%s)' % (col_name)


def upper(col_name):
    return 'UPPER(%s)' % (col_name)


def remnl(col_name):
    return 'REPLACE(%s, CHR(13), \'\')' % (col_name)


def trim(col_name):
    return 'TRIM(%s)' % (col_name)


def pclean(col, action_list):
    p_col = 'p_' + col
    prefix = 'v_' + col + ' := '
    postfix = ';'
    return pclean_helper(p_col, action_list, prefix, postfix)


def pclean_helper(col, action_list, prefix=None, postfix=None):
    out = col
    for fun_name in action_list:
        fun = action_fun_map[fun_name]
        out = fun(out)
    if prefix:
        out = prefix + out
    if postfix:
        out = out + postfix
    return out


def lookup(col, action_list):
    '''
    LOOKUP: { 'High School'   : ['HS', 'HIGH SCHOOL'],
              'Middle School' : ['MS', 'MIDDLE SCHOOL'],
              'Elementary School' : ['ES' 'ELEMENTARY SCHOOL']
            }
    '''
    ret = ''
    pref = '\n\tIF   '
    for canon_value, accepted_value_list in action_list.items():
        ret += lookup_helper(pref, col, canon_value, accepted_value_list)
        pref = '\n\tELSIF'
    return ret


def lookup_helper(prefix, col, val, val_list):
    pref2 = '\n\tOR   '
    ret = make_substring_part(prefix, col, val_list[0])
    for i in range(1, len(val_list)):
        ret += make_substring_part(pref2, col, val_list[i])
    ret += " THEN\n\t\tv_result := '{value}';".format(value=val)
    return ret


def make_substring_part(pref, col, val, length=None):
    if not length:
        length = len(val)
    return "{prefix} SUBSTRING(t_{col_name}, 1, {length}) = '{value}'".format(prefix=pref, col_name=col, length=len(val), value=val)


action_fun_map = {'lower': lower, 'upper': upper, 'remnl': remnl, 'trim': trim,
                  PCLEAN: pclean, LOOKUP: lookup}
