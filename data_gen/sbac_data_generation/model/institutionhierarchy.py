"""
Model an institution hierarchy as defined for SBAC.

@author: nestep
@date: February 24, 2014
"""


class InstitutionHierarchy:
    """
    Model an institution hierarchy.
    """
    def __init__(self):
        self.rec_id = None
        self.guid = None
        self.state = None
        self.district = None
        self.school = None
        self.from_date = None
        self.to_date = None

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'institution_hierarchy': self}
