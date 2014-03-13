"""
Model the SBAC-specific items of a student.

@author: nestep
@date: March 3, 2014
"""

from mongoengine import BooleanField, DateTimeField, IntField, ReferenceField, StringField

from general.model.district import District
from general.model.student import Student


class SBACStudent(Student):
    """
    The SBAC-specific student class.
    """
    district = ReferenceField(District, required=True)
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