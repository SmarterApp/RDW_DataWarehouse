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

__author__ = 'abrien'

from edudl2.rule_maker.makers import datacalculation as dc

DAZE_CORRECT = 'daze_correct'

FORMULA = 'formula'
NAME = 'name'

__default_prep = ['upper', 'remnl', 'trim']

transformation_calculate = {
    DAZE_CORRECT: {
        FORMULA: '({daze_incorrect}-{daze_adjusted})/2',
        NAME: 'calculate_daze_correct'
    }
}


def parse_dict(key):
    '''
    For different kinds of rules, this function returns
    corresponding function to generate rule and list of parameters
    '''

    parts = transformation_calculate.get(key)
    col = parts.get('col', key)
    prepare = parts.get('prepare', __default_prep)
    parm = [col, prepare]

    # Assume (for now) that this is valid SQL
    # TODO: Sanitize this SQL command.
    formula = parts[FORMULA]
    column_name = key
    function_name = parts[NAME]
    sql_statement = dc.create_calculated_value_sql_function(formula)
    return func, parm

if __name__ == '__main__':
    pass
