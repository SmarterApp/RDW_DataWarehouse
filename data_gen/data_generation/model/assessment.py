"""Model the core of an assessment.

:author: nestep
:date: February 24, 2014
"""

from data_generation import run_id as global_run_id


class Assessment:
    """The core assessment class.
    """
    def __init__(self):
        self.run_id = global_run_id
        self.guid = None

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - assessment

        :returns: Dictionary of root objects
        """
        return {'assessment': self}
