"""
Model the SBAC-specific items of a student.

@author: nestep
@date: March 3, 2014
"""

from mongoengine import BooleanField, DateTimeField, IntField, ReferenceField, StringField

from data_generation.model.student import Student
from sbac_data_generation.model.district import SBACDistrict
from sbac_data_generation.model.registrationsystem import SBACRegistrationSystem
from sbac_data_generation.model.state import SBACState


class SBACStudent(Student):
    """
    The SBAC-specific student class.
    """
    rec_id = IntField(required=True)
    rec_id_sr = IntField(required=True)
    state = ReferenceField(SBACState, required=True)
    district = ReferenceField(SBACDistrict, required=True)
    reg_sys = ReferenceField(SBACRegistrationSystem, required=False)
    guid_sr = StringField(required=True, max_length=30)
    external_ssid = StringField(required=True, max_length=40)
    external_ssid_sr = StringField(required=True, max_length=30)
    school_entry_date = DateTimeField(required=False)
    prg_migrant = BooleanField(required=False)
    prg_idea = BooleanField(required=False)
    lang_code = StringField(required=False, max_length=3)
    lang_prof_level = StringField(required=False, max_length=20)
    lang_title_3_prg = StringField(required=False, max_length=30)
    prg_lep_entry_date = DateTimeField(required=False)
    prg_lep_exit_date = DateTimeField(required=False)
    prg_primary_disability = StringField(required=False, max_length=30)
    derived_demographic = IntField(required=False)

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        :returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'registration_system': self.reg_sys,
                'student': self}
