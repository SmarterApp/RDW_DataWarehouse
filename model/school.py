"""
Model the SBAC-specific items of a school.

@author: nestep
@date: February 22, 2014
"""

from mongoengine import StringField

from general.model.school import School


class SBACSchool(School):
    """
    The SBAC-specific school class.
    """
    guid_sr = StringField(required=True)