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
