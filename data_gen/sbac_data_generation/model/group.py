"""
Model the SBAC-specific items of a teaching staff.

@author: gkathuria
@date: June 19, 2014
"""

from mongoengine import StringField, IntField, ReferenceField, Document
from sbac_data_generation.model.school import SBACSchool


class SBACgroup(Document):
    """
    Model a SBAC student group.
    """
    type = StringField(required=True)
    guid_sr = StringField(required=True)
    school = ReferenceField(SBACSchool, required=True)
    id = IntField(required=True)
    name = StringField(required=True)
