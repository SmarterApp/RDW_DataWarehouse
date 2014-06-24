"""
Model the SBAC-specific items of a teaching staff.

@author: gkathuria
@date: June 19, 2014
"""

from mongoengine import StringField

from data_generation.model.staff import TeachingStaff


class SBACTeachingStaff(TeachingStaff):
    """
    The SBAC-specific TeachingStaff class.
    """
    guid_sr = StringField(required=True)
