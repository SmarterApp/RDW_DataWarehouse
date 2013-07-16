'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from sqlalchemy.sql.expression import true, false


def getDemographicFilter(filter_name, filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: filters applifed query
    '''
    filter_map = {Constants_filter_names.YES: true(),
                  Constants_filter_names.NO: false(),
                  Constants_filter_names.NOT_STATED: None
                  }
    disabled_filter = []
    target_filter = filters.get(filter_name, None)
    if target_filter:
        for f in target_filter:
            try:
                disabled_filter.append(filter_map[f])
            except:
                pass
    return disabled_filter
