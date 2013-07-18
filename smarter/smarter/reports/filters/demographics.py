'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from sqlalchemy.sql.expression import true, false, or_


def getDemographicFilter(filter_name, column, filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: list of filters to be applied to query
    '''
    filter_map = {Constants_filter_names.YES: true(),
                  Constants_filter_names.NO: false(),
                  Constants_filter_names.NOT_STATED: None
                  }
    where_clause = None
    disabled_filter = []
    target_filter = filters.get(filter_name, None)
    if target_filter:
        for f in target_filter:
            try:
                disabled_filter.append(column == filter_map[f])
            except:
                pass
    if disabled_filter:
        if len(disabled_filter) == 1:
            where_clause = disabled_filter[0]
        else:
            where_clause = or_(disabled_filter)
    return where_clause
