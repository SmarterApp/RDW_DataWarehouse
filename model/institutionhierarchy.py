"""
Model an institution hierarchy as defined for SBAC.

@author: nestep
@date: February 24, 2014
"""

from mongoengine import BooleanField, DateTimeField, Document, IntField, ReferenceField, StringField

from general.model.district import District
from general.model.school import School
from general.model.state import State


class InstitutionHierarchy(Document):
    """
    Model an institution hierarchy.
    """
    rec_id = IntField(required=True)
    guid = StringField(required=True)
    state = ReferenceField(State, required=True)
    district = ReferenceField(District, required=True)
    school = ReferenceField(School, required=True)
    from_date = DateTimeField(required=True)
    to_date = DateTimeField(required=False)
    most_recent = BooleanField(required=True)

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'institution_hierarchy': self}