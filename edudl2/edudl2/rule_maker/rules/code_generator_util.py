'''
Created on June 13, 2013

@author: lichen
'''
from edudl2.rule_maker.rules.rule_keys import LOWER, UPPER, REMNL, TRIM, PCLEAN, VCLEAN, RCLEAN, LOOKUP, TO_CHAR, INLIST, OUTLIST, MIN0, COMPARE_LENGTH
from edudl2.rule_maker.rules.code_generator_sql_template import for_loop_exp, length_exp, index_exp, substr_exp, repace_exp, tochar_exp, min0_exp


def lower(code_version, col_name):
    '''
    Function to generate lower case expression
    '''
    return 'LOWER(%s)' % (col_name)


def upper(code_version, col_name):
    '''
    Function to generate upper case expression
    '''
    return 'UPPER(%s)' % (col_name)


def remnl(code_version, col_name):
    '''
    Function to generate removing spaces expression
    '''
    return repace_exp[code_version].format(col_name=col_name)


def trim(code_version, col_name):
    '''
    Function to generate trim expression
    '''
    return 'TRIM(%s)' % (col_name)


def to_char(code_version, col_name):
    '''
    Function to generate to char expression
    '''
    return tochar_exp[code_version].format(col_name=col_name)


def min0(code_version, col_name):
    return min0_exp[code_version].format(col_name=col_name)


def vclean(code_version, col, action_list):
    '''
    Function to generate code for notation 'VCLEAN'
    '''
    p_col = 'v_' + col
    prefix = 't_' + col + ' := '
    postfix = ';'
    return clean_helper(code_version, p_col, action_list, prefix, postfix)


def pclean(code_version, col, action_list):
    '''
    Function to generate code for notation 'PCLEAN'
    '''
    p_col = 'p_' + col
    prefix = 'v_' + col + ' := '
    postfix = ';'
    return clean_helper(code_version, p_col, action_list, prefix, postfix)


def rclean(code_version, col, action_list):
    '''
    Function to generate code for notation 'PCLEAN'
    '''
    """
    p_col = 'v_result'
    prefix = 'v_result' + ' := '
    postfix = ';'
    return clean_helper(code_version, p_col, action_list, prefix, postfix)
    """

    rclean_list = []
    # list of action
    if isinstance(action_list, list):
        for action in action_list:
            fun = action_fun_map[action]
            rclean_list.append(fun(code_version, 'v_result'))
    # just one action
    else:
        fun = action_fun_map[action_list]
        rclean_list.append(fun(code_version, 'v_result'))
    return ''.join(rclean_list)


def clean_helper(code_version, col, action_list, prefix=None, postfix=None):
    out = col
    if isinstance(action_list, list):
        for fun_name in action_list:
            fun = action_fun_map[fun_name]
            out = fun(code_version, out)
    else:
            fun = action_fun_map[action_list]
            out = fun(code_version, out)
    if prefix:
        out = prefix + out
    if postfix:
        out = out + postfix
    return out


def lookup(code_version, col, action_dict):
    '''
    Function to generate code for notation 'LOOKUP'
    LOOKUP: { 'High School'   : ['HS', 'HIGH SCHOOL'],
              'Middle School' : ['MS', 'MIDDLE SCHOOL'],
              'Elementary School' : ['ES' 'ELEMENTARY SCHOOL']
            }
    '''
    # sort the dict
    sorted_keys = sorted(action_dict.keys())
    ret = ''
    pref = '\n\tIF   '
    for canon_value in sorted_keys:
        accepted_value_list = action_dict[canon_value]
        ret += lookup_helper(code_version, pref, col, canon_value, accepted_value_list)
        pref = '\n\tELSIF'
    return ret


def lookup_helper(code_version, prefix, col, val, val_list):
    pref2 = '\n\tOR   '
    ret = make_substring_part(code_version, prefix, col, val_list[0])
    for i in range(1, len(val_list)):
        if val_list[i]:
            ret += make_substring_part(code_version, pref2, col, val_list[i])
        else:
            ret += make_null_part(code_version, pref2, col)
    # return ''.join([' THEN\n\t\t', assignment('v_result', '\'{value}\'')]).format(value=val)
    ret += " THEN\n\t\tv_result := '{value}';".format(value=val)
    return ret


def make_substring_part(code_version, pref, col, val, length=None):
    if not length:
        length = len(val)
    substring_str = substr_exp[code_version]
    return "{prefix} {substring_str}(t_{col_name}, 1, {length}) = '{value}'".format(prefix=pref, substring_str=substring_str, col_name=col, length=len(val), value=val)


def make_null_part(code_version, pref, col):
    return "{prefix} (t_{col_name}) IS NULL".format(prefix=pref, col_name=col)


def assignment(left_exp, right_exp, **parm):
    '''
    Function to generate assignment expression
    '''
    concat = ''.join([left_exp, ' := ', right_exp, ';'])
    if parm and len(parm) > 0:
        return concat.format(**parm)
    return concat


def inlist(code_version, col, inlist, **parm):
    '''
    Function to generate code for notation 'INLIST'
    '''
    initialize_v_result = assignment('v_result', '\'NOT FOUND\'') + '\n'
    return initialize_v_result + make_for_loop_exp(code_version, col, **parm)


def make_for_loop_exp(code_version, col, **parm):
    '''
    Function to generate for_loop expression
    Reference: https://github.wgenhq.net/Ed-Ware-SBAC/udl/blob/master/sql/udl_stg/pkg/pb_loader.sql#L691
    '''
    count_value = 'keys_' if OUTLIST in parm.keys() else 'vals_'
    compare_length = parm[COMPARE_LENGTH] if COMPARE_LENGTH in parm.keys() else None
    if_statement = if_statment_for_compare_length(code_version, compare_length, count_value, col)
    return for_loop_exp[code_version].format(col_name=col, count_value=count_value, if_statement=if_statement)


def if_statment_for_compare_length(code_version, compare_length, count_value, col):
    '''
    Function to generate if statement for COMPARE_LENGTH
    '''
    sub_str = substr_exp[code_version]
    index_str = index_exp[code_version]
    length_str = length_exp[code_version]
    template = ''
    if compare_length:
        template = """IF {sub_str}(t_{col_name}, 1, {length}) = {sub_str}({count_value}{col_name}{index_str}, 1, {length}) THEN"""
    else:
        template = """IF {sub_str}(t_{col_name}, 1, {length_str}({count_value}{col_name}{index_str})) = {count_value}{col_name}{index_str} THEN"""
    return template.format(sub_str=sub_str, col_name=col, length_str=length_str, index_str=index_str, length=compare_length, count_value=count_value)


def fun_name(*parts):
    '''
    Function to generate a function name by given parts
    '''
    return ''.join(*parts)

action_fun_map = {LOWER: lower,
                  UPPER: upper,
                  REMNL: remnl,
                  TRIM: trim,
                  PCLEAN: pclean,
                  VCLEAN: vclean,
                  RCLEAN: rclean,
                  LOOKUP: lookup,
                  TO_CHAR: to_char,
                  MIN0: min0,
                  INLIST: inlist}
