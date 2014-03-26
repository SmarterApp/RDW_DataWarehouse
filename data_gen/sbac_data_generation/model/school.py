"""
Model the SBAC-specific items of a school.

@author: nestep
@date: February 22, 2014
"""

from mongoengine import BooleanField, StringField

from data_generation.model.school import School


class SBACSchool(School):
    """
    The SBAC-specific school class.
    """
    guid_sr = StringField(required=True)
    takes_interim_asmts = BooleanField(required=True, default=False)