"""
Model the SBAC-specific items of a district.

@author: nestep
@date: February 22, 2014
"""

from mongoengine import StringField, BooleanField

from data_generation.model.district import District


class SBACDistrict(District):
    """
    The SBAC-specific district class.
    """
    student_grouping = BooleanField(required=True, default=False)
    guid_sr = StringField(required=True)
