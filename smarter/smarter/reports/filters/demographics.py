'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from edapi import utils
from sqlalchemy.sql.expression import true, false

DEMOGRAPHICS_SELECTED_VALUE = utils.enum(YES=1, NO=2, NOT_STATED=4, NONE=0)

def getValue(filters, filterName):
    rtn_value = DEMOGRAPHICS_SELECTED_VALUE.NONE
    for _filter in filters.get(filterName, []):
        if _filter.upper() == 'Y':
            rtn_value |= DEMOGRAPHICS_SELECTED_VALUE.YES
        elif _filter.upper() == 'N':
            rtn_value |= DEMOGRAPHICS_SELECTED_VALUE.NO
        elif _filter.upper() == 'NS':
            rtn_value |= DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED
    return rtn_value


def getDemographicProgramIepFilter(fact_asmt_outcome, filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: filters applifed query
    '''
    disabled_filter = []
    if filters:
        dmg_prg_iep = getValue(filters, Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP)
        if dmg_prg_iep != DEMOGRAPHICS_SELECTED_VALUE.NONE:
            in_value = []
            if dmg_prg_iep & DEMOGRAPHICS_SELECTED_VALUE.YES:
                in_value.append(true())
            if dmg_prg_iep & DEMOGRAPHICS_SELECTED_VALUE.NO:
                in_value.append(false())
            if dmg_prg_iep & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED:
                in_value.append(None)
            disabled_filter.append(fact_asmt_outcome.c.dmg_prg_iep.in_(in_value))
    return disabled_filter


def getDemographicProgram504Filter(fact_asmt_outcome, filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: filters applifed query
    '''
    disabled_filter = []
    if filters:
        dmg_prg_504 = getValue(filters, Constants_filter_names.DEMOGRAPHICS_PROGRAM_504)
        if dmg_prg_504 != DEMOGRAPHICS_SELECTED_VALUE.NONE:
            in_value = []
            if dmg_prg_504 & DEMOGRAPHICS_SELECTED_VALUE.YES:
                in_value.append(true())
            if dmg_prg_504 & DEMOGRAPHICS_SELECTED_VALUE.NO:
                in_value.append(false())
            if dmg_prg_504 & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED:
                in_value.append(None)
            disabled_filter.append(fact_asmt_outcome.c.dmg_prg_504.in_(in_value))
    return disabled_filter
