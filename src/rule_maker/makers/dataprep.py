'''
Created on May 29, 2013

@author: kallen
'''


# ====== functions to implement basic data preparation ======
def __upper(inner):
    return 'UPPER(%s)' % (inner)


def __remnl(inner):
    return 'REPLACE(%s, CHR(13), \'\')' % (inner)


def __trim(inner):
    return 'TRIM(%s)' % (inner)
# ===========================================================

# ====== map of data preparation functions ==================
__fun_map = {'upper': __upper, 'remnl': __remnl, 'trim': __trim}
# ===========================================================

# ====== default data preparation list ======================
__default_prep = ['upper', 'remnl', 'trim']
# ===========================================================


def do_data_prep(col, dp_list=__default_prep, prefix=None, postfix=None):
    out = col
    for fun_name in dp_list:
        fun = __fun_map[fun_name]
        out = fun(out)
    if prefix:
        out = prefix + out
    if postfix:
        out = out + postfix
    return out


def do_col_prep(col, dp_list=__default_prep):
    p_col = 'p_' + col
    prefix = 'v_' + col + ' := '
    postfix = ';'
    return do_data_prep(p_col, dp_list, prefix, postfix)

if __name__ == '__main__':
    pass
