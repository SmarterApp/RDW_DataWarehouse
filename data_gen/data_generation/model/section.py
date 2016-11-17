"""Model the core of a section.

:author: nestep
:date: February 24, 2014
"""

from data_generation import run_id as global_run_id


class Section:
    """The core of a section.
    """
    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.clss = None
        self.teachers = []
        self.name = None
        self.grade = None
        self.from_date = None
        self.to_date = None
        self.most_recent = None

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
        return {'state': self.clss.school.district.state,
                'district': self.clss.school.district,
                'school': self.clss.school,
                'class': self.clss,
                'section': self}
