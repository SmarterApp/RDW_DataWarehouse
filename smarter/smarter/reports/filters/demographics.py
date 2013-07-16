'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from edapi import utils
from sqlalchemy.sql.expression import true, false

DEMOGRAPHICS_SELECTED_VALUE = utils.enum(YES=1, NO=2, NOT_STATED=4, NONE=0)


def getValue(filters, filterName):
    '''
    return filter value in integer
    '''
    rtn_value = DEMOGRAPHICS_SELECTED_VALUE.NONE
    for _filter in filters.get(filterName, []):
        if _filter.upper() == Constants_filter_names.YES:
            rtn_value |= DEMOGRAPHICS_SELECTED_VALUE.YES
        elif _filter.upper() == Constants_filter_names.NO:
            rtn_value |= DEMOGRAPHICS_SELECTED_VALUE.NO
        elif _filter.upper() == Constants_filter_names.NOT_STATED:
            rtn_value |= DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED
    return rtn_value


def getDemographicProgramIepFilter(filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: filters applifed query
    '''
    disabled_filter = []
    if filters:
        dmg_prg_iep = getValue(filters, Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP)
        if dmg_prg_iep != DEMOGRAPHICS_SELECTED_VALUE.NONE:
            if dmg_prg_iep & DEMOGRAPHICS_SELECTED_VALUE.YES:
                disabled_filter.append(true())
            if dmg_prg_iep & DEMOGRAPHICS_SELECTED_VALUE.NO:
                disabled_filter.append(false())
            if dmg_prg_iep & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED:
                disabled_filter.append(None)
    return disabled_filter


def getDemographicProgram504Filter(filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: filters applifed query
    '''
    disabled_filter = []
    if filters:
        dmg_prg_504 = getValue(filters, Constants_filter_names.DEMOGRAPHICS_PROGRAM_504)
        if dmg_prg_504 != DEMOGRAPHICS_SELECTED_VALUE.NONE:
            if dmg_prg_504 & DEMOGRAPHICS_SELECTED_VALUE.YES:
                disabled_filter.append(true())
            if dmg_prg_504 & DEMOGRAPHICS_SELECTED_VALUE.NO:
                disabled_filter.append(false())
            if dmg_prg_504 & DEMOGRAPHICS_SELECTED_VALUE.NOT_STATED:
                disabled_filter.append(None)
    return disabled_filter
