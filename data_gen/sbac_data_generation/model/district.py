"""
Model the SBAC-specific items of a district.

@author: nestep
@date: February 22, 2014
"""

from data_generation.model.district import District


class SBACDistrict(District):
    """
    The SBAC-specific district class.
    """
    def __init__(self):
        super().__init__()
        self.student_grouping = None
        self.guid_sr = None
