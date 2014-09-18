"""
Model the SBAC-specific items of a student.

@author: nestep
@date: March 3, 2014
"""

from data_generation.model.student import Student


class SBACStudent(Student):
    """
    The SBAC-specific student class.
    """
    def __init__(self):
        super().__init__()
        self.rec_id = None
        self.rec_id_sr = None
        self.state = None
        self.district = None
        self.reg_sys = None
        self.guid_sr = None
        self.external_ssid = None
        self.external_ssid_sr = None
        self.school_entry_date = None
        self.prg_migrant = None
        self.prg_idea = None
        self.lang_code = None
        self.lang_prof_level = None
        self.lang_title_3_prg = None
        self.prg_lep_entry_date = None
        self.prg_lep_exit_date = None
        self.prg_primary_disability = None
        self.derived_demographic = None
        self.group_1_id = None
        self.group_1_text = None
        self.group_2_id = None
        self.group_2_text = None
        self.group_3_id = None
        self.group_3_text = None
        self.group_4_id = None
        self.group_4_text = None
        self.group_5_id = None
        self.group_5_text = None
        self.group_6_id = None
        self.group_6_text = None
        self.group_7_id = None
        self.group_7_text = None
        self.group_8_id = None
        self.group_8_text = None
        self.group_9_id = None
        self.group_9_text = None
        self.group_10_id = None
        self.group_10_text = None

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        :returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'registration_system': self.reg_sys,
                'student': self}
