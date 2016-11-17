"""Model the generals of a student.

:author: nestep
:date: February 22, 2014
"""

from data_generation import run_id as global_run_id


class Student:
    """The core student class.
    """
    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.school = None
        self.grade = None
        self.gender = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.dob = None
        self.email = None
        self.address_line_1 = None
        self.address_line_2 = None
        self.address_city = None
        self.address_zip = None
        self.eth_white = False
        self.eth_black = False
        self.eth_hispanic = False
        self.eth_asian = False
        self.eth_pacific = False
        self.eth_amer_ind = False
        self.eth_multi = False
        self.eth_none = False
        self.prg_iep = None
        self.prg_sec504 = None
        self.prg_lep = None
        self.prg_econ_disad = None
        self.held_back = False

    @property
    def name(self):
        """The full name of student.
        """
        if self.middle_name is not None:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name
        else:
            return self.first_name + ' ' + self.last_name

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        :returns: Dictionary of root objects
        """
        return {'state': self.school.district.state,
                'district': self.school.district,
                'school': self.school,
                'student': self}
