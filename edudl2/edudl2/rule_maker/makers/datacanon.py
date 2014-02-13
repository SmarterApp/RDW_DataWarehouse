'''
Created on May 29, 2013

@author: kallen
'''

from edudl2.rule_maker.makers.dataprep import do_col_prep

# data canonicalization

# https://github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0/blob/master/src/fileloader/transformation_rules.sql

__map_func_top = """
CREATE OR REPLACE FUNCTION {func_name}
(
    p_{col_name} IN VARCHAR
)
RETURNS VARCHAR AS
$$
DECLARE
    v_{col_name} VARCHAR(255);
    v_return VARCHAR(255);
BEGIN
    """

__map_func_end = """
    ELSE
        v_return := v_{col_name};
    END IF;

    RETURN v_return;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql;
    """

__lists_func_top1 = """
CREATE OR REPLACE FUNCTION map_{col_name}
(
    p_{col_name}  IN  VARCHAR
)
RETURNS VARCHAR AS
$$
DECLARE
    v_{col_name}      VARCHAR(255);
    v_return          VARCHAR(255);
    v_sub{col_name}   VARCHAR(255);

    vals_{col_name} text[] = ARRAY['{value_list}'];

"""
__lists_func_top2 = """
    keys_{col_name} text[] = ARRAY['{key_list}'];
"""
__lists_func_top3 = """
BEGIN
"""

__lists_func_end = """
IF v_return = 'NOT FOUND' THEN
    v_return := v_{col_name};
END IF;

RETURN v_return;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};

END;
$$ LANGUAGE plpgsql;"""


def make_substring_part(pref, col, val, length=None):
    if not length:
        length = len(val)
    return "{prefix} SUBSTRING(v_{col_name}, 1, {length}) = '{value}'".format(prefix=pref, col_name=col, length=len(val), value=val)


def make_substring(prefix, col, val, val_list):
    pref2 = '\n\tOR   '
    ret = make_substring_part(prefix, col, val_list[0])
    for i in range(1, len(val_list)):
        ret += make_substring_part(pref2, col, val_list[i])
    ret += " THEN\n\t\tv_return := '{value}';".format(value=val)
    return ret


def make_substring_list(col, cf):
    ret = ''
    pref = '\n\tIF   '
    for key in list(cf.keys()):
        val = key
        val_list = cf[key]
        ret += make_substring(pref, col, val, val_list)
        pref = '\n\tELSIF'
    return ret


def make_function_for_look_up(col, dp_list, comes_from):
    '''
    Main function to generate transformation rules
    which has the logic the same as map_gender
    '''
    func_top = __map_func_top.format(col_name=col, func_name='map_' + col)
    col_prep = do_col_prep(col, dp_list)
    func_mid = col_prep + make_substring_list(col, comes_from)
    func_end = __map_func_end.format(col_name=col)

    func = func_top + func_mid + func_end

    return func


def make_function_for_lists(col, dp_list, value_list, compare_length, check_n=None, key_list=None):
    '''
    Main function to generate transformation rules that accepts one or two input lists
    '''
    func_top = create_lists_func_top(col, value_list, key_list)
    col_prep = do_col_prep(col, dp_list)
    sub_value = present_sub_value(col, compare_length)
    func_mid = col_prep + sub_value + make_for_loop_check(col, check_n, compare_length, key_list is not None)
    func_end = __lists_func_end.format(col_name=col)
    func = func_top + func_mid + func_end
    return func


def create_lists_func_top(col, value_list, key_list):
    top_statement = __lists_func_top1.format(col_name=col, value_list="\',\'".join(value_list))
    if key_list is not None:
        top_statement += __lists_func_top2.format(col_name=col, key_list="\',\'".join(key_list))
    top_statement += __lists_func_top3
    return top_statement


def present_sub_value(col, compare_length):
    '''
    Make a sub string expression
    '''
    return '\nv_sub{col_name} :=SUBSTRING(v_{col_name}, 1, {compare_length});\n'.format(col_name=col, compare_length=compare_length)


def make_for_loop_check(col, check_n, compare_length, has_key_and_value):
    '''
    Make a for loop logic.
    Reference: https://github.wgenhq.net/Ed-Ware-SBAC/udl/blob/master/sql/udl_stg/pkg/pb_loader.sql#L691
    '''
    part1 = assign_return_value('NOT FOUND')
    if check_n is not None:
        if_exp = make_or_exp(col, list(check_n.values())[0], compare_length)
        then_exp = assign_return_value(list(check_n.keys())[0])
        else_exp = make_for_loop_exp(col, compare_length, has_key_and_value)
        part2 = make_if_then_else_exp(if_exp, then_exp, else_exp)
    else:
        part2 = make_for_loop_exp(col, compare_length, has_key_and_value)
    return part1 + part2


def make_or_exp(col, accepted_value, compare_length):
    '''
    Make a serious of 'or' expression
    '''
    if len(accepted_value) > 1:
        ret = ''
        prefix = ''
        for value in list(accepted_value):
            ret += prefix + 'v_{col_name} = \'{value}\''.format(col_name=col, value=value)
            prefix = '\n\tOR '
        return ret
    else:
        return make_substring_part('', col, accepted_value[0], compare_length)


def assign_return_value(expected_value):
    '''
    Make a assignment expression to parameter v_return
    '''
    return 'v_return :=\'{assigned_value}\';\n'.format(assigned_value=expected_value)


def make_if_then_else_exp(if_exp, then_exp, else_exp=None):
    '''
    Make a if-else-then expression
    '''
    basic = 'IF {if_exp} THEN \n\t{then_exp}'.format(if_exp=if_exp, then_exp=then_exp)
    if else_exp:
        basic = basic + '\nELSE\n{else_exp}'.format(else_exp=else_exp)
    basic += '\n END IF;'
    return basic


def make_for_loop_exp(col, compare_length, has_key_and_value):
    count_value = 'keys_' if has_key_and_value is True else 'vals_'
    template = """
    FOR cntr IN array_lower({count_value}{col_name}, 1)..array_upper({count_value}{col_name}, 1)
    LOOP
        IF v_sub{col_name} = SUBSTRING({count_value}{col_name}[cntr], 1, {length}) THEN
            v_return := vals_{col_name}[cntr];
            EXIT;
        END IF;
    END LOOP;
    """.format(col_name=col, length=compare_length, count_value=count_value)
    return template
