"""
Model the SBAC-specific items of a teaching staff.

@author: gkathuria
@date: June 19, 2014
"""

from data_generation.model.staff import TeachingStaff


class SBACTeachingStaff(TeachingStaff):
    """
    The SBAC-specific TeachingStaff class.
    """
    def __init__(self):
        super().__init__()
        self.guid_sr = None
