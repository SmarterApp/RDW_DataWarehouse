'''
Created on Jun 10, 2013

@author: kallen

Validation rules for first validation.

UDL pipeline currently has four possible transformation/validation phases

transformation #1: simple clean-up and canonicalization
validation #1 : basic value and type checks
transformation #2: data type conversions
validation #2 : match against existing business data values

'''

from validation_rule_sql import *
import random
import sys


BYCOLUMN = 'by_column'  # keyed by column name - rule applies only to this column
BYRULE = 'by_rule'  # keyed by rule name - rule needs to look at multiple columns


## **** Rule application ****
EACH = 'each'  # (default) a rule applies to a single column and checks (in parallel) EACH row
                            # put an entry into the ERR table for each bad row
                            # (was ROW rule in old-UDL)
ALL = 'all'  # only an error if every row fails for this column (COLUMN rule in old-UDL)
                            # put ONE entry in ERR table, and only if ALL rows are bad for this column
                            # (was COL rule in old-UDL)
BOTH = 'both'  # if ALL rows are bad, then one entry in ERR table
                            # if not, then check EACH row
                            # (this magically happens in old-UDL)
## **** Rule Checks ****
# # We will express checks in a positive manner (assert) - if the condition is true there is no error

ISNOTNULL = 'not_null'  # error if value is null
DATE = 'date'  # parameter=date-format, check that the given column (a VARCHAR) corresponds to a date with the given format
MINDATE = 'min_date'  # parameter=date-value, check that the given column (a VARCHAR) has a date value not less than the given date-value
UNIQUE = 'unique'  # error if column value is not unique across all rows --- perhaps this can assume 'ALL'
REGEX = 'regex'  # validate the column against the given regex
ALPHA = {REGEX: '[A-Za-z]'}
GUID = {REGEX: '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'}
AFTER_2001 = {MINDATE: '2001-01-01'}


## **** BYRULE stuff ****
ASSERT = 'assert'  # an expression (in a string) including column names in {} which if FALSE means there is an error
NAME = 'name'  # name of this error check (validation)
ALLNULL = 'all_null'

__validation_rules_definition = {BYCOLUMN: {'guid_asmt': [ISNOTNULL],  # for EACH row where guid_teacher is null, put record id in ERR table
                                            'guid_student': [ISNOTNULL, ALL],  # record one error in ERR table if in ALL rows guid_student is NULL
                                            'guid_assessment': [ISNOTNULL, BOTH],  # combination of ALL then EACH
                                            'date_assessed': [ISNOTNULL, {DATE:'YYYY-MM-DD'}],  # check EACH date not null, and has the given format
                                            'dob_student': [ISNOTNULL, AFTER_2001, ALL],  # record 1 error if ALL dob_student are NULL or if all dob_student are less than Jan 1st 2001
                                            'guid_staff': [[ISNOTNULL, ALL], [UNIQUE, EACH]],
                                            'name_student_first': ALPHA,
                                            'guid_inst_hier': GUID

                                 },

#                                BYRULE: { 'sumto100' : ['measure1', 'measure2', 'measure3'], # checks that the sum of these 3 columns is exactly 100
#                                          'sumtox': {'total':1200, 'columns':['colABC', 'colXYZ']},  # checks that colABC + colXYZ == 1200
#                                          NULL: ['dob_student', 'dob_teacher'], # record an error for EACH row where both the dob_student AND dob_teacher are NULL
#                                        }

                                 BYRULE: [{NAME:'check-123', ASSERT:'{measure1}+{measure2}+{measure3}=100'},
                                          {NAME:'checkABCXYZ', ASSERT: '{colABC}+{colXYZ}!=1200'},
                                          {NAME:'both-dob-null', ALLNULL:['dob_student', 'dob_teacher']}
                                          ]
                  }


# dictionary to map notation and corresponding sql
__validation_notation_sql_dict = {ISNOTNULL: {ALL: NULL_ALL_SQL, EACH: NULL_SQL, BOTH: 'TBD'},
                                  DATE: DATE_FORMAT_SQL,
                                  # AFTER_2001: 'TBD',
                                  UNIQUE: UNIQUE_SQL,
                                  # ALPHA: 'TBD',
                                  # GUID: 'TBD'
                               }


__validation_rules_error_code = {}


def by_column_func(column_name, rules_for_column, **para):
    para['column'] = column_name
    sql_stat = []
    # check the items in rules_for_column
    if isinstance(rules_for_column, list):
        # individual notation defined, e.g. [ISNOTNULL, ALL]
        if not all(isinstance(n, list) for n in rules_for_column):
            sql_stat = get_sql_for_notations(rules_for_column, **para)
        # list of notations defined. e.g. [[ISNOTNULL, ALL], [UNIQUE, EACH]]
        else:
            for one_rule_set in rules_for_column:
                sql_stat.extend(get_sql_for_notations(one_rule_set, **para))
    else:
        # single notation
        pass
    return sql_stat


def by_rule_func(rule_content, **parm):
    pass


def get_sql_for_notations(rules_for_column, **parm):
    scope = EACH
    if ALL in rules_for_column:
        scope = ALL
    elif BOTH in rules_for_column:
        scope = BOTH
    # get rest of notations
    notations = [rule for rule in rules_for_column if rule is not scope]
    sql_stat = []
    for notation in notations:
        parm['error_code'] = get_error_code_for_notation(notation, scope)
        if notation in list(__validation_notation_sql_dict.keys()):
            if notation == ISNOTNULL:
                sql_stat_template = __validation_notation_sql_dict[ISNOTNULL][scope]
            elif notation == UNIQUE:
                sql_stat_template = __validation_notation_sql_dict[UNIQUE]
        elif isinstance(notation, dict):
            if DATE in list(notation.keys()):
                sql_stat_template = __validation_notation_sql_dict[DATE]
                parm['date_format'] = notation[DATE]
        # replace value in template
        sql_statement = sql_stat_template.format(**parm)
        sql_stat.append(sql_statement)
    return sql_stat


def get_error_code_for_notation(notation, scope):
    # TODO: TBD
    return random.randint(1, 1000)


def generate_validation_proc(para):
    '''
    Main function to generate validation procedures
    '''
    sql_stat = []
    for rule_type, rule_content in __validation_rules_definition.items():
        func = __validation_rules_func[rule_type]
        # BYRULE
        if isinstance(rule_content, list):
            temp = func(rule_content, **para)
            if temp is not None:
                sql_stat.extend(func(rule_content, **para))
        # BYCOLUMN
        elif isinstance(rule_content, dict):
            for column_name, rules_for_column in rule_content.items():
                temp = func(column_name, rules_for_column, **para)
                if temp is not None:
                    sql_stat.extend(temp)
        else:
            print("error")
    return sql_stat


__validation_rules_func = {BYCOLUMN: by_column_func,
                           BYRULE: by_rule_func}


if __name__ == '__main__':
    para = {'batch_id': 'be310a4c-e2db-4237-8c73-57d7a4f355a3',
            'err_source': 6,
            'schema': 'udl2',
            'table': 'INT_SBAC_ASMT_OUTCOME'
    }
    validation_proc = generate_validation_proc(para)
    for proc in validation_proc:
        sys.stdout.write(proc)
