"""
Create output filters for data values that are specific to the SBAC project.

@author: nestep
@date: February 28, 2014
"""

import random


def filter_yesno(val):
    """
    Filter a True/False value as Yes/No.

    @param val: The value to filter
    @returns: Yes or No if value is True or False respectively
    """
    return 'Yes' if val else 'No'


def filter_yesnoblank(val):
    """
    Filter a True/False value as Yes/No, but when no have a 8% chance that the value will be blank.

    @param val: The value to filter
    @returns: Yes or No if value is True or False respectively, but 8% of time 'No' will be blank.
    """
    return 'Yes' if val else 'No' if random.randint(1, 100) < 93 else ''


def filter_always_true(val):
    """
    Always return True.

    @param val: The value that is ignored
    @returns: True
    """
    return True


SBAC_FILTERS = {
    'yesno': filter_yesno,
    'yesnoblank': filter_yesnoblank,
    'always_true': filter_always_true
}