'''
Created on May 29, 2013

@author: kallen
'''

from rule_maker.makers.dataprep import do_col_prep

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
        v_return := v_{col_name}
    END IF;

    RETURN v_return;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql
    """

__lists_func_top1 = """
FUNCTION map_{col_name}
(
    p_{col_name}  IN  VARCHAR
)
RETURNS VARCHAR AS
$$
DECLARE
    v_{col_name}      VARCHAR(255);
    v_return          VARCHAR(255);
"""
__lists_func_top2 = """
    v_sub{col_name}   VARCHAR(255);
"""
__lists_func_top3 = """
    -- need to change to the postgres syntax to
    TYPE arr{col_name}_t IS VARRAY(21) OF VARCHAR2(32);
         vals_{col_name} arr{col_name}_t := arr{col_name}_t('{value_list}');
"""
__lists_func_top4 = """
         keys_{col_name} arr{col_name}_t := arr{col_name}_t('{key_list}');
"""
__lists_func_top5 = """
BEGINE
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
$$ LANGUAGE plpgsql"""


def make_substring_part(pref, col, val, length=None):
    if not length:
        length = len(val)
    return "{prefix} SUBSTRING(v_{col_name}, 1, {length}) = '{value}'".format(prefix=pref, col_name=col, length=len(val), value=val)


def make_substring(prefix, col, val, val_list):
    pref2 = '\n\tOR   '
    ret = make_substring_part(prefix, col, val_list[0])
    for i in range(1, len(val_list)):
        ret += make_substring_part(pref2, col, val_list[i])
    ret += " THEN\n\t\tv_return := '{value}'".format(value=val)
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


def make_function_for_map(col, dp_list, comes_from):
    func_top = __map_func_top.format(col_name=col, func_name='map_' + col)
    col_prep = do_col_prep(col, dp_list)
    func_mid = col_prep + make_substring_list(col, comes_from)
    func_end = __map_func_end.format(col_name=col)

    func = func_top + func_mid + func_end

    return func


def make_function_for_lists(col, dp_list, key_list, value_list, check_n, compare_length):
    func_top = create_lists_func_top(True, True)
    __two_lists_func_top.format(col_name=col, func_name='map_' + col, key_list='\',\''.join(key_list), value_list='\',\''.join(value_list))
    col_prep = do_col_prep(col, dp_list)
    sub_value = present_sub_value(col, compare_length)
    func_mid = col_prep + sub_value + make_for_loop_check(col, check_n, compare_length)
    func_end = __lists_func_end.format(col_name=col)
    func = func_top + func_mid + func_end
    print(func)


def create_lists_func_top(has_key_and_value, has_subStr):
    top_statement = __lists_func_top1
    if has_subStr:
        top_statement += __lists_func_top2
    top_statement += __lists_func_top3
    if has_key_and_value:
        top_statement += __lists_func_top4
    top_statement += __lists_func_top5
    return top_statement


def present_sub_value(col, compare_length):
    return '\nv_sub{col_name} :=SUBSTRING(v_{col_name}, 1, {compare_length});\n'.format(col_name=col, compare_length=compare_length)


def make_for_loop_check(col, check_n, compare_length):
    pre1 = assign_return_value('NOT FOUND')
    if_exp = make_substring_part('', col, list(check_n.values())[0][0], compare_length)
    then_exp = assign_return_value(list(check_n.keys())[0])
    else_exp = make_for_loop_exp(col, compare_length)
    pre2 = make_if_then_else_exp(if_exp, then_exp, else_exp)
    return pre1 + pre2


def assign_return_value(expected_value):
    return 'v_return :=\'{assigned_value}\';\n'.format(assigned_value=expected_value)


def make_if_then_else_exp(if_exp, then_exp, else_exp=None):
    basic = 'IF {if_exp} THEN \n\t{then_exp}'.format(if_exp=if_exp, then_exp=then_exp)
    if else_exp:
        basic = basic + '\nELSE\n{else_exp}'.format(else_exp=else_exp)
    basic += '\n END IF;'
    return basic


def make_for_loop_exp(col, compare_length):
    template = """
    FOR cntr IN 1..keys_{col_name}.COUNT
    LOOP
        IF v_sub{col_name} = SUBSTRING(keys_{col_name}(cntr), 1, {length}) THEN
            v_return := vals_{col_name}(cntr);
            EXIT;
        END IF;
    END LOOP;
    """.format(col_name=col, length=compare_length)
    return template
