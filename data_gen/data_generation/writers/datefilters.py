"""Create output filters for data values.

:author: nestep
:date: March 6, 2014
"""

import datetime


def filter_date_Y_m_d(val):
    """Filter a Date/Time value as %Y-%m-%d.

    :param val: The value to filter
    :returns: %Y-%m-%d format of Date/Time
    """
    if val is None:
        return ''
    if type(val) is str:
        val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    return val.strftime('%Y-%m-%d')


def filter_date_Ymd(val):
    """Filter a Date/Time value as %Y%m%d.

    :param val: The value to filter
    :returns: %Y%m%d format of Date/Time
    """
    if val is None:
        return ''
    if type(val) is str:
        val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    return val.strftime('%Y%m%d')


def filter_date_Y(val):
    """Filter a Date/Time value as %Y.

    :param val: The value to filter
    :returns: %Y format of Date/Time
    """
    if val is None:
        return ''
    if type(val) is str:
        val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    return val.strftime('%Y')


def filter_date_m(val):
    """Filter a Date/Time value as %m.

    :param val: The value to filter
    :returns: %m format of Date/Time
    """
    if val is None:
        return ''
    if type(val) is str:
        val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    return val.strftime('%m')


def filter_date_d(val):
    """Filter a Date/Time value as %d.

    :param val: The value to filter
    :returns: %d format of Date/Time
    """
    if val is None:
        return ''
    if type(val) is str:
        val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
    return val.strftime('%d')


FILTERS = {
    'date_Y_m_d': filter_date_Y_m_d,
    'date_Ymd': filter_date_Ymd,
    'date_Y': filter_date_Y,
    'date_m': filter_date_m,
    'date_d': filter_date_d
}
