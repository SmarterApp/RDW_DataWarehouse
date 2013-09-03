'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from sqlalchemy.sql.expression import true, false, or_, null


# Maps Yes, No and Not Stated to equivalent SQLAlchemey values
filter_map = {Constants_filter_names.YES: true(),
              Constants_filter_names.NO: false(),
              Constants_filter_names.NOT_STATED: null()}


# Used in report_config for allowing demographics parameters for reports
DEMOGRAPHICS_CONFIG = {
    Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
        }
    },
    Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
        }
    },
    Constants_filter_names.DEMOGRAPHICS_PROGRAM_504: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
        }
    },
    Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
        }
    },
    Constants_filter_names.DEMOGRAPHICS_ETHNICITY: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN + "|" +
            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC + "|" +
            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_MULTI + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_NOT_STATED + ")$",
        }
    },
    Constants_filter_names.DEMOGRAPHICS_GRADE: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(3|4|5|6|7|8|11)$"
        }
    },
    Constants_filter_names.DEMOGRAPHICS_GENDER: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants_filter_names.DEMOGRAPHICS_GENDER_MALE + "|" + Constants_filter_names.DEMOGRAPHICS_GENDER_FEMALE + "|" + Constants_filter_names.DEMOGRAPHICS_GENDER_NOT_STATED + ")$"
        }
    }
}


def get_demographic_filter(filter_name, column, filters):
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


def has_demographics_filters(params):
    '''
    Returns true if params contain demographics filter related key

    :param dict params: map of key value pair
    '''
    has_filters = False
    if (Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP in params or
            Constants_filter_names.DEMOGRAPHICS_PROGRAM_504 in params or
            Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP in params or
            Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1 in params or
            Constants_filter_names.DEMOGRAPHICS_GRADE in params or
            Constants_filter_names.DEMOGRAPHICS_ETHNICITY in params or
            Constants_filter_names.DEMOGRAPHICS_GENDER in params):
        has_filters = True
    return has_filters


def apply_demographics_filter_to_query(query, fact_asmt_outcome, filters):
    '''
    Apply demographics filters to a query

    :param query:  a sqlalchemy query
    :param fact_asmt_outcome:  reference to fact_asmt_outcome table
    :param dict filters: dictionary that contains filter related key value
    '''
    if filters:
        filter_iep = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP, fact_asmt_outcome.c.dmg_prg_iep, filters)
        if filter_iep is not None:
            query = query.where(filter_iep)
        filter_504 = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_504, fact_asmt_outcome.c.dmg_prg_504, filters)
        if filter_504 is not None:
            query = query.where(filter_504)
        filter_lep = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP, fact_asmt_outcome.c.dmg_prg_lep, filters)
        if filter_lep is not None:
            query = query.where(filter_lep)
        filter_tt1 = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1, fact_asmt_outcome.c.dmg_prg_tt1, filters)
        if filter_tt1 is not None:
            query = query.where(filter_tt1)
        filter_grade = filters.get(Constants_filter_names.DEMOGRAPHICS_GRADE)
        if filters.get(Constants_filter_names.DEMOGRAPHICS_GRADE):
            query = query.where(fact_asmt_outcome.c.asmt_grade.in_(filter_grade))
        filter_eth = filters.get(Constants_filter_names.DEMOGRAPHICS_ETHNICITY)
        if filter_eth is not None:
            query = query.where(fact_asmt_outcome.c.dmg_eth_derived.in_(filter_eth))
        filter_gender = filters.get(Constants_filter_names.DEMOGRAPHICS_GENDER)
        if filter_gender is not None:
            query = query.where(fact_asmt_outcome.c.gender.in_(filter_gender))
    return query
