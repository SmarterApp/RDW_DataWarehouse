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

from edudl2.validation_rule_sql import *
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
ISUNIQUE = 'unique'  # error if column value is not unique across all rows --- perhaps this can assume 'ALL'
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
                                            'date_assessed': [ISNOTNULL, {DATE: 'YYYY-MM-DD'}],  # check EACH date not null, and has the given format
                                            'dob_student': [ISNOTNULL, AFTER_2001, ALL],  # record 1 error if ALL dob_student are NULL or if all dob_student are less than Jan 1st 2001
                                            'guid_staff': [[ISNOTNULL, ALL], [ISUNIQUE, EACH]],
                                            'name_student_first': ALPHA,
                                            'guid_inst_hier': GUID
                                            },

                                 #==============================================
                                 # BYRULE: { 'sumto100' : ['measure1', 'measure2', 'measure3'], # checks that the sum of these 3 columns is exactly 100
                                 #          'sumtox': {'total':1200, 'columns':['colABC', 'colXYZ']},  # checks that colABC + colXYZ == 1200
                                 #          NULL: ['dob_student', 'dob_teacher'], # record an error for EACH row where both the dob_student AND dob_teacher are NULL}
                                 #==============================================

                                 BYRULE: [{NAME: 'check-123', ASSERT: '{measure1}+{measure2}+{measure3}=100'},
                                          {NAME: 'checkABCXYZ', ASSERT: '{colABC}+{colXYZ}!=1200'},
                                          {NAME: 'both-dob-null', ALLNULL: ['dob_student', 'dob_teacher']}
                                          ]}


# dictionary to map notation and corresponding sql
__validation_notation_sql_dict = {ISNOTNULL: {ALL: NULL_ALL_SQL, EACH: NULL_SQL, BOTH: '\nGOING TO GENERATE SQL FOR ISNOTNULL -- BOTH\n'},
                                  DATE: DATE_FORMAT_SQL,
                                  MINDATE: '\nGOING TO GENERATE SQL FOR MINDATE RULE\n',
                                  ISUNIQUE: UNIQUE_SQL,
                                  REGEX: '\nGOING TO GENERATE SQL FOR REGEX RULE\n',
                                  # GUID: 'TBD'
                                  }


__validation_rules_error_code = {}


def by_column_func(column_name, rules_for_column, **para):
    # print(column_name, rules_for_column)
    para['column'] = column_name
    scope = EACH
    sql_stat = []
    # check the type of items in rules_for_column
    if isinstance(rules_for_column, list):
        for one_rule_set in rules_for_column:
            if one_rule_set in [ALL, EACH, BOTH]:
                continue
            # pattern 1 -- list of notations defined. e.g. [[ISNOTNULL, ALL], [ISUNIQUE, EACH]]
            if isinstance(one_rule_set, list):
                sql_stat.extend(by_column_func(column_name, one_rule_set, **para))
                # print("recursive once,", one_rule_set, column_name, len(sql_stat))

            # pattern 2 -- dictionary, e.g. {action: parameter}
            elif isinstance(one_rule_set, dict):
                for action, parameters in one_rule_set.items():
                    para = construct_parameters(action, parameters, para)
                    sql_stat.extend(get_sql_for_notation(action, scope, ** para))

            # pattern 3 -- individual action, but not ALL, EACH or BOTH
            elif one_rule_set not in [ALL, EACH, BOTH]:
                # individual notation defined, e.g. [ISNOTNULL, ALL]
                if ALL in rules_for_column:
                    scope = ALL
                elif BOTH in rules_for_column:
                    scope = BOTH
                sql_stat = get_sql_for_notation(one_rule_set, scope, ** para)
            else:
                print("error", column_name, one_rule_set)
                raise Exception
    else:
        # single notation
        sql_stat = by_column_func(column_name, [rules_for_column], **para)
    return sql_stat


def by_rule_func(rule_content, **parm):
    '''
    Main function to process by_rule validation notations
    #TODO: TO BE WRITTEN
    '''
    return []


def construct_parameters(action, parameters, para):
    # TODO: make it for all cases
    if action == DATE:
        para['date_format'] = parameters
    return para


def get_sql_for_notation(notation, scope, **parm):
    # print('get_sql_for_notation', notation)
    sql_stat_template = ''

    # get rest of notations
    sql_stat = []
    parm['error_code'] = get_error_code_for_notation(notation, scope)
    if notation in list(__validation_notation_sql_dict.keys()):
        if notation == ISNOTNULL:
            sql_stat_template = __validation_notation_sql_dict[ISNOTNULL][scope]
        else:
            sql_stat_template = __validation_notation_sql_dict[notation]

    # replace value in template
    sql_statement = sql_stat_template.format(**parm)
    if len(sql_statement) > 0:
        # print("One rule is generated for %s" % notation)
        sql_stat.append(sql_statement)
    return sql_stat


def get_error_code_for_notation(notation, scope):
    # TODO: need to write code to get error code
    return random.randint(1, 1000)


# This is the dictionary to map validation rule category and corresponding function
__validation_rules_func = {BYCOLUMN: by_column_func,
                           BYRULE: by_rule_func}


def generate_validation_proc(para):
    '''
    Main function to generate validation procedures
    '''
    sql_stat = []
    for rule_type, rule_content in __validation_rules_definition.items():
        func = __validation_rules_func[rule_type]
        # BYRULE
        if isinstance(rule_content, list):
            sql_stat.extend(func(rule_content, **para))
        # BYCOLUMN
        elif isinstance(rule_content, dict):
            for column_name, rules_for_column in rule_content.items():
                sql_stat.extend(func(column_name, rules_for_column, **para))
        else:
            # can be replaced by raising exception
            print("error")
    return sql_stat


if __name__ == '__main__':
    para = {'guid_batch': 'be310a4c-e2db-4237-8c73-57d7a4f355a3',
            'err_source': 6,
            'schema': 'udl2',
            'table': 'INT_SBAC_ASMT_OUTCOME'}
    validation_proc = generate_validation_proc(para)
    print("Generated %i number of rules" % len(validation_proc))
    for proc in validation_proc:
        sys.stdout.write(proc)
