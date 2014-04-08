"""
Model the SBAC-specific items of a section.

@author: nestep
@date: March 14, 2014
"""

from mongoengine import IntField, ReferenceField

from data_generation.model.section import Section
from sbac_data_generation.model.district import SBACDistrict
from sbac_data_generation.model.school import SBACSchool
from sbac_data_generation.model.state import SBACState


class SBACSection(Section):
    """
    The SBAC-specific section class.
    """
    rec_id = IntField(required=True)
    school = ReferenceField(SBACSchool, required=True)
    district = ReferenceField(SBACDistrict, required=True)
    state = ReferenceField(SBACState, required=True)

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - state
          - district
          - school
          - class
          - section

        :returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'class': self.clss,
                'section': self}
