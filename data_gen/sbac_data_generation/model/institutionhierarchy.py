"""
Model an institution hierarchy as defined for SBAC.

@author: nestep
@date: February 24, 2014
"""

from mongoengine import DateTimeField, Document, IntField, ReferenceField, StringField

from sbac_data_generation.model.district import SBACDistrict
from sbac_data_generation.model.school import SBACSchool
from sbac_data_generation.model.state import SBACState


class InstitutionHierarchy(Document):
    """
    Model an institution hierarchy.
    """
    rec_id = IntField(required=True)
    guid = StringField(required=True, primary_key=True)
    state = ReferenceField(SBACState, required=True)
    district = ReferenceField(SBACDistrict, required=True)
    school = ReferenceField(SBACSchool, required=True)
    from_date = DateTimeField(required=True)
    to_date = DateTimeField(required=False)

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'institution_hierarchy': self}