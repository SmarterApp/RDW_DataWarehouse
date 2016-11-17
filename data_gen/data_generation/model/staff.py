"""Model the core of different staff members.

:author: nestep
:date: February 22, 2014
"""

from data_generation import run_id as global_run_id


class Staff:
    """The core staff class.
    """
    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.gender = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None

    @property
    def name(self):
        """The full name of the staff member.
        """
        if self.middle_name is not None:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name
        else:
            return self.first_name + ' ' + self.last_name


class DistrictStaff(Staff):
    """Specifics for a district-level staff member.
    """
    def __init__(self):
        super().__init__()
        self.district = None


class TeachingStaff(Staff):
    """Specifics for a teaching staff member.
    """
    def __init__(self):
        super().__init__()
        self.school = None
