"""
Model the SBAC-specific items of a school.

@author: nestep
@date: February 22, 2014
"""

from data_generation.model.school import School


class SBACSchool(School):
    """
    The SBAC-specific school class.
    """
    def __init__(self):
        super().__init__()
        self.guid_sr = None
        self.takes_interim_asmts = False
