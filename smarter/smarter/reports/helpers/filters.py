'''
Created on Jul 11, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import true, false, or_, null
from smarter.reports.helpers.constants import Constants

YES = 'Y'
NO = 'N'
NOT_STATED = 'NS'
NONE = 'NONE'


FILTERS_PROGRAM_504 = 'dmgPrg504'
FILTERS_PROGRAM_IEP = 'dmgPrgIep'
FILTERS_PROGRAM_LEP = 'dmgPrgLep'
FILTERS_PROGRAM_ECD = 'dmgStsEcd'
FILTERS_PROGRAM_MIG = 'dmgStsMig'

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

FILTERS_GROUP_1 = 'group1Id'
FILTERS_GROUP_2 = 'group2Id'
FILTERS_GROUP_3 = 'group3Id'
FILTERS_GROUP_4 = 'group4Id'
FILTERS_GROUP_5 = 'group5Id'
FILTERS_GROUP_6 = 'group6Id'
FILTERS_GROUP_7 = 'group7Id'
FILTERS_GROUP_8 = 'group8Id'
FILTERS_GROUP_9 = 'group9Id'
FILTERS_GROUP_10 = 'group10Id'

# Maps Yes, No and Not Stated to equivalent SQLAlchemey values
filter_map = {YES: true(),
              NO: false(),
              NOT_STATED: null()}


reverse_filter_map = {None: NOT_STATED,
                      True: YES,
                      False: NO}


# Maps between client and server demographics names
dmg_map = {Constants.DMG_PRG_IEP: FILTERS_PROGRAM_IEP,
           Constants.DMG_PRG_504: FILTERS_PROGRAM_504,
           Constants.DMG_PRG_LEP: FILTERS_PROGRAM_LEP,
           Constants.DMG_STS_ECD: FILTERS_PROGRAM_ECD,
           Constants.DMG_STS_MIG: FILTERS_PROGRAM_MIG}


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
    FILTERS_PROGRAM_ECD: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + YES + "|" + NO + ")$",
        }
    },
    FILTERS_PROGRAM_MIG: {
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
    },
    FILTERS_GROUP_1: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_2: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_3: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_4: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_5: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_6: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_7: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_8: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_9: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
        }
    },
    FILTERS_GROUP_10: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9\-]{0,50}$"
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


def apply_filter_to_query(query, fact_asmt_outcome_vw, dim_student, filters):
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
        filter_ecd = _get_filter(FILTERS_PROGRAM_ECD, fact_asmt_outcome_vw.c.dmg_sts_ecd, filters)
        if filter_ecd is not None:
            query = query.where(filter_ecd)
        filter_mig = _get_filter(FILTERS_PROGRAM_MIG, fact_asmt_outcome_vw.c.dmg_sts_mig, filters)
        if filter_mig is not None:
            query = query.where(filter_mig)
        filter_grade = filters.get(FILTERS_GRADE)
        if filters.get(FILTERS_GRADE):
            query = query.where(fact_asmt_outcome_vw.c.asmt_grade.in_(filter_grade))
        filter_eth = filters.get(FILTERS_ETHNICITY)
        if filter_eth is not None:
            query = query.where(fact_asmt_outcome_vw.c.dmg_eth_derived.in_(filter_eth))
        filter_sex = filters.get(FILTERS_SEX)
        if filter_sex is not None:
            query = query.where(fact_asmt_outcome_vw.c.sex.in_(filter_sex))
        filter_group_1 = filters.get(FILTERS_GROUP_1)
        if filter_group_1 is not None:
            query = query.where(dim_student.c.group_1_id.in_(filter_group_1))
        filter_group_2 = filters.get(FILTERS_GROUP_2)
        if filter_group_2 is not None:
            query = query.where(dim_student.c.group_2_id.in_(filter_group_2))
        filter_group_3 = filters.get(FILTERS_GROUP_3)
        if filter_group_3 is not None:
            query = query.where(dim_student.c.group_3_id.in_(filter_group_3))
        filter_group_4 = filters.get(FILTERS_GROUP_4)
        if filter_group_4 is not None:
            query = query.where(dim_student.c.group_4_id.in_(filter_group_4))
        filter_group_5 = filters.get(FILTERS_GROUP_5)
        if filter_group_5 is not None:
            query = query.where(dim_student.c.group_5_id.in_(filter_group_5))
        filter_group_6 = filters.get(FILTERS_GROUP_6)
        if filter_group_6 is not None:
            query = query.where(dim_student.c.group_6_id.in_(filter_group_6))
        filter_group_7 = filters.get(FILTERS_GROUP_7)
        if filter_group_7 is not None:
            query = query.where(dim_student.c.group_7_id.in_(filter_group_7))
        filter_group_8 = filters.get(FILTERS_GROUP_8)
        if filter_group_8 is not None:
            query = query.where(dim_student.c.group_8_id.in_(filter_group_8))
        filter_group_9 = filters.get(FILTERS_GROUP_9)
        if filter_group_9 is not None:
            query = query.where(dim_student.c.group_9_id.in_(filter_group_9))
        filter_group_10 = filters.get(FILTERS_GROUP_10)
        if filter_group_10 is not None:
            query = query.where(dim_student.c.group_10_id.in_(filter_group_10))
    return query


def get_student_demographic(result):
    '''
    Formats student demographic data for consumption in front end
    '''
    demographic = {}

    for column in dmg_map.keys():
        demographic[dmg_map.get(column)] = reverse_filter_map.get(result[column])
    demographic[FILTERS_ETHNICITY] = str(result[Constants.DMG_ETH_DERIVED])
    demographic[FILTERS_SEX] = result[FILTERS_SEX]

    return demographic
