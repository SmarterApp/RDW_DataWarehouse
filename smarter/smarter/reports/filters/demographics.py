'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names


def getBoolean(filters, filterName):
    value = None
    for _filter in filters:
        if _filter[0] == filterName:
            value = _filter[1]
            if value is not None:
                if type(value) == str:
                    value = True if value.toLower() == 'true' else False
            break
    return value 

def getDisabledFilter(fact_asmt_outcome, filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: filters applifed query
    '''
    disabled_filter = []
    if filters:
        dmg_prg_iep = getBoolean(filters, Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP)
        dmg_prg_504 = getBoolean(filters, Constants_filter_names.DEMOGRAPHICS_PROGRAM_504)
        if dmg_prg_iep is not None:
            disabled_filter.append(fact_asmt_outcome.c.dmg_prg_iep == dmg_prg_iep)
        if dmg_prg_504 is not None:
            disabled_filter.append(fact_asmt_outcome.c.dmg_prg_504 == dmg_prg_504)
    return disabled_filter
