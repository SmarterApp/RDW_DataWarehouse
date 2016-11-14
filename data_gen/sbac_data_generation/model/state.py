"""
Model the SBAC-specific items of a state.

@author: nestep
@date: February 22, 2014
"""

from data_generation.model.state import State


class SBACState(State):
    """
    The SBAC-specific state class.
    """
    def __init__(self):
        super().__init__()
        self.guid_sr = None
