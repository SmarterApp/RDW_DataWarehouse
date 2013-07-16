'''
Created on May 9, 2013

@author: kallen
'''


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

__map_comes_from = {'M': ['M', 'B'], 'F': ['F', 'G'], 'NS': ['NS', 'NOT_SPECIFIED', 'NOT SPECIFIED']}


def make_substring_part(pref, col, val):
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
    for key in sorted(cf.keys()):
        val = key
        val_list = cf[key]
        ret += make_substring(pref, col, val, val_list)
        pref = '\n\tELSIF'
    return ret


def make_function(col):
    func_top = __map_func_top.format(col_name=col, func_name='map_' + col)
    func_mid = make_substring_list(col, __map_comes_from)
    func_end = __map_func_end.format(col_name=col)

    func = func_top + func_mid + func_end

    return func


def doit(inner):
    func = make_function('gender')
    return func


if __name__ == '__main__':
    pass
