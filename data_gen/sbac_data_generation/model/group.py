"""
Model the SBAC-specific items of a teaching staff.

@author: gkathuria
@date: June 19, 2014
"""


class SBACgroup:
    """
    Model a SBAC student group.
    """
    def __init__(self):
        self.type = None
        self.guid_sr = None
        self.school = None
        self.id = None
        self.name = None
