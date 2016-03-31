# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'tshewchuk'


"""
This module contains utility functions used in report data generation.
"""


def percentage(count, total):
    """
    Safe percentage calculating function.

    @param count: Count for some category for the year
    @param total: Total for the year

    @return: Adjusted percentage of count to total (int or None)
    """

    if count is not None and total:
        return (count / total) * 100
    else:
        return None


def subtract(subtractor, subtractee):
    """
    Safe subtraction calculating function.

    @param subtractor: Number from which to subtract subtractee
    @param subtractee: Number which to subtract from subtractor

    @return: Adjusted subtraction of subtractee from subtractor (int or None)
    """

    if subtractor is not None and subtractee is not None:
        return subtractor - subtractee
    else:
        return None


def format_floatval(floatval):
    """
    Convert floating point value to formatted string for report.

    @param floatval: Floating point value

    @return: Formatted string representation of floating point value
    """
    if floatval is not None:
        return str(round(floatval, 2)).rstrip('0').rstrip('.')
    else:
        return ''


def format_intval(intval):
    """
    Convert integer value to formatted string for report.

    @param intval: Integer value

    @return: Formatted string representation of integer value
    """
    if intval is not None:
        return str(intval)
    else:
        return ''


def get_row_identifiers(key, tracker):
    state_name = key.state_name
    district_name = key.district_name if key.district_name else 'ALL'
    school_name = key.school_name if key.school_name else 'ALL'
    category, value = tracker.get_category_and_value()

    return state_name, district_name, school_name, category, value
