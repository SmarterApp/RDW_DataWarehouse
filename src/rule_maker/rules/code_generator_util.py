'''
Created on June 13, 2013

@author: lichen
'''
from rule_maker.rules.rule_keys import PCLEAN, VCLEAN, LOOKUP, INLIST, DATE, CALCULATE
from rule_maker.rules.code_generator_sql_template import POSTGRES, ORACLE, for_loop_exp


def lower(code_version, col_name):
    return 'LOWER(%s)' % (col_name)


def upper(code_version, col_name):
    return 'UPPER(%s)' % (col_name)


def remnl(code_version, col_name):
    if code_version is POSTGRES:
        return 'REPLACE(%s, CHR(13), \'\')' % (col_name)
    elif code_version is ORACLE:
        return 'REPLACE(%s, CHR(13), NULL)' % (col_name)
    else:
        print('Do not support version %s' % code_version)
        raise Exception


def trim(code_version, col_name):
    return 'TRIM(%s)' % (col_name)


def pclean(code_version, col, action_list):
    p_col = 'p_' + col
    prefix = 'v_' + col + ' := '
    postfix = ';'
    return pclean_helper(code_version, p_col, action_list, prefix, postfix)


def pclean_helper(code_version, col, action_list, prefix=None, postfix=None):
    out = col
    for fun_name in action_list:
        fun = action_fun_map[fun_name]
        out = fun(code_version, out)
    if prefix:
        out = prefix + out
    if postfix:
        out = out + postfix
    return out


def lookup(code_version, col, action_list):
    '''
    LOOKUP: { 'High School'   : ['HS', 'HIGH SCHOOL'],
              'Middle School' : ['MS', 'MIDDLE SCHOOL'],
              'Elementary School' : ['ES' 'ELEMENTARY SCHOOL']
            }
    '''
    ret = ''
    pref = '\n\tIF   '
    for canon_value, accepted_value_list in action_list.items():
        ret += lookup_helper(code_version, pref, col, canon_value, accepted_value_list)
        pref = '\n\tELSIF'
    return ret


def lookup_helper(code_version, prefix, col, val, val_list):
    pref2 = '\n\tOR   '
    ret = make_substring_part(code_version, prefix, col, val_list[0])
    for i in range(1, len(val_list)):
        ret += make_substring_part(code_version, pref2, col, val_list[i])
    ret += " THEN\n\t\tv_result := '{value}';".format(value=val)
    return ret


def make_substring_part(code_version, pref, col, val, length=None):
    if not length:
        length = len(val)
    substring_exp = substring(code_version)
    if code_version is POSTGRES:
        return "{prefix} {substring_exp}(t_{col_name}, 1, {length}) = '{value}'".format(prefix=pref, substring_exp=substring_exp, col_name=col, length=len(val), value=val)


def substring(code_version):
    if code_version == ORACLE:
        return 'SUBSTR'
    elif code_version == POSTGRES:
        return 'SUBSTRING'
    else:
        print('Do not support version %s' % code_version)
        raise Exception


def assignment(left_exp, right_exp, parm=None):
    concat = ''.join([left_exp, ' := ', right_exp, ';'])
    if parm:
        return concat.format(**parm)
    return concat


def inlist(code_version, col, inlist, compare_length, outlist):
    initialize_v_result = assignment('v_result', '\'NOT FOUND\'', {}) + '\n'
    return initialize_v_result + make_for_loop_exp(code_version, col, compare_length, outlist is not None)


def array_exp(code_version, value_list, para_name):
    # add code for code_version
    return """{para_name} text[] = ARRAY['{value_list}'];""".format(para_name=para_name, value_list="\',\'".join(value_list))


def make_for_loop_exp(code_version, col, compare_length, has_key_and_value):
    '''
    Make a for loop logic.
    Reference: https://github.wgenhq.net/Ed-Ware-SBAC/udl/blob/master/sql/udl_stg/pkg/pb_loader.sql#L691
    '''
    count_value = 'keys_' if has_key_and_value is True else 'vals_'
    if_statement = if_statment_for_compare_length(code_version, compare_length, count_value, col)
    return for_loop_exp[code_version].format(col_name=col, length=compare_length, count_value=count_value, if_statement=if_statement)


def if_statment_for_compare_length(code_version, compare_length, count_value, col):
    # TODO:ADD CODE FOR code_version
    if compare_length:
        return """IF SUBSTRING(t_{col_name}, 1, {length}) = SUBSTRING({count_value}{col_name}[cntr], 1, {length}) THEN""".format(col_name=col, length=compare_length, count_value=count_value)
    else:
        return """IF SUBSTRING(t_{col_name}, 1, CHAR_LENGTH({count_value}{col_name}[cntr])) = {count_value}{col_name}[cntr] THEN""".format(col_name=col, length=compare_length, count_value=count_value)

action_fun_map = {'lower': lower,
                  'upper': upper,
                  'remnl': remnl,
                  'trim': trim,
                  PCLEAN: pclean,
                  LOOKUP: lookup,
                  INLIST: inlist}
