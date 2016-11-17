"""Model the core of an assessment outcome (an instance of a student taking an assessment).

:author: nestep
:date: February 24, 2014
"""

from data_generation import run_id as global_run_id


class AssessmentOutcome:
    """The core assessment outcome class.
    """
    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.student = None
        self.assessment = None
        self.date_taken = None

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - state
          - district
          - school
          - student
          - section
          - assessment
          - assessment_outcome

        :returns: Dictionary of root objects
        """
        return {'state': self.student.school.district.state,
                'district': self.student.school.district,
                'school': self.student.school,
                'student': self.student,
                'assessment': self.assessment,
                'assessment_outcome': self}
