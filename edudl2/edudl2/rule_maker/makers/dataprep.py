# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
