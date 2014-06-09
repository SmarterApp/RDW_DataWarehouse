'''
Created on Jul 11, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import true, false, or_, null

YES = 'Y'
NO = 'N'
NOT_STATED = 'NS'
NONE = 'NONE'


FILTERS_PROGRAM_504 = 'dmgPrg504'
FILTERS_PROGRAM_IEP = 'dmgPrgIep'
FILTERS_PROGRAM_LEP = 'dmgPrgLep'

FILTERS_ETHNICITY_AMERICAN = '4'
FILTERS_ETHNICITY_ASIAN = '2'
FILTERS_ETHNICITY_BLACK = '1'
FILTERS_ETHNICITY_HISPANIC = '3'
FILTERS_ETHNICITY_PACIFIC = '5'
FILTERS_ETHNICITY_WHITE = '6'
# Two or more races
FILTERS_ETHNICITY_MULTI = '7'
FILTERS_ETHNICITY_NOT_STATED = '0'

FILTERS_SEX_MALE = 'male'
FILTERS_SEX_FEMALE = 'female'
FILTERS_SEX_NOT_STATED = 'not_stated'

FILTERS_GRADE = 'grade'
FILTERS_ETHNICITY = 'ethnicity'
FILTERS_SEX = 'sex'

# Maps Yes, No and Not Stated to equivalent SQLAlchemey values
filter_map = {YES: true(),
              NO: false(),
              NOT_STATED: null()}


def reverse_filter_map(value):
    if value is null():
        return NOT_STATED
    elif value:
        return YES
    else:
        return NO


# Used in report_config for allowing demographics parameters for reports
FILTERS_CONFIG = {
    FILTERS_PROGRAM_LEP: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + YES + "|" + NO + "|" + NOT_STATED + ")$",
        }
    },
    FILTERS_PROGRAM_IEP: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + YES + "|" + NO + "|" + NOT_STATED + ")$",
        }
    },
    FILTERS_PROGRAM_504: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + YES + "|" + NO + "|" + NOT_STATED + ")$",
        }
    },
    FILTERS_ETHNICITY: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + FILTERS_ETHNICITY_AMERICAN + "|" + FILTERS_ETHNICITY_ASIAN + "|" +
            FILTERS_ETHNICITY_BLACK + "|" + FILTERS_ETHNICITY_HISPANIC + "|" + FILTERS_ETHNICITY_PACIFIC + "|" +
            FILTERS_ETHNICITY_MULTI + "|" + FILTERS_ETHNICITY_WHITE + "|" + FILTERS_ETHNICITY_NOT_STATED + ")$",
        }
    },
    FILTERS_GRADE: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(3|4|5|6|7|8|11)$"
        }
    },
    FILTERS_SEX: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + FILTERS_SEX_MALE + "|" + FILTERS_SEX_FEMALE + "|" + FILTERS_SEX_NOT_STATED + ")$"
        }
    }
}


def _get_filter(filter_name, column, filters):
    '''
    Apply filters for Disability

    :rtype: sqlalchemy.sql.select
    :returns: list of filters to be applied to query
    '''
    where_clause = None
    expr = []
    target_filter = filters.get(filter_name, None)
    if target_filter:
        for f in target_filter:
            try:
                expr.append(column == filter_map[f])
            except:
                pass
    if expr:
        where_clause = or_(*expr)
    return where_clause


def has_filters(params):
    '''
    Returns true if params contain filter related key

    :param dict params: map of key value pair
    '''
    return not params.keys().isdisjoint(FILTERS_CONFIG.keys())


def apply_filter_to_query(query, fact_asmt_outcome_vw, filters):
    '''
    Apply demographics filters to a query

    :param query:  a sqlalchemy query
    :param fact_asmt_outcome:  reference to fact_asmt_outcome table
    :param dict filters: dictionary that contains filter related key value
    '''
    if filters:
        filter_iep = _get_filter(FILTERS_PROGRAM_IEP, fact_asmt_outcome_vw.c.dmg_prg_iep, filters)
        if filter_iep is not None:
            query = query.where(filter_iep)
        filter_504 = _get_filter(FILTERS_PROGRAM_504, fact_asmt_outcome_vw.c.dmg_prg_504, filters)
        if filter_504 is not None:
            query = query.where(filter_504)
        filter_lep = _get_filter(FILTERS_PROGRAM_LEP, fact_asmt_outcome_vw.c.dmg_prg_lep, filters)
        if filter_lep is not None:
            query = query.where(filter_lep)
        filter_grade = filters.get(FILTERS_GRADE)
        if filters.get(FILTERS_GRADE):
            query = query.where(fact_asmt_outcome_vw.c.asmt_grade.in_(filter_grade))
        filter_eth = filters.get(FILTERS_ETHNICITY)
        if filter_eth is not None:
            query = query.where(fact_asmt_outcome_vw.c.dmg_eth_derived.in_(filter_eth))
        filter_sex = filters.get(FILTERS_SEX)
        if filter_sex is not None:
            query = query.where(fact_asmt_outcome_vw.c.sex.in_(filter_sex))
    return query


def get_student_demographic(result):
    demographic = {}

    for column in ['dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504']:
        filter_name, value = _column_to_filter(column, result[column])
        demographic[filter_name] = value
     # 'dmg_eth_derived'
    demographic['ethnicity'] = str(result['dmg_eth_derived'])
    demographic['gender'] = result['sex']

    return demographic


def _column_to_filter(column, value):
    if column == 'dmg_prg_iep':
        return (FILTERS_PROGRAM_IEP, reverse_filter_map(value))
    elif column == 'dmg_prg_504':
        return (FILTERS_PROGRAM_504, reverse_filter_map(value))
    elif column == 'dmg_prg_lep':
        return (FILTERS_PROGRAM_LEP, reverse_filter_map(value))
    return (column, value)
