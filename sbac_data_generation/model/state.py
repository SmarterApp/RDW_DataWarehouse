"""
Model the SBAC-specific items of a state.

@author: nestep
@date: February 22, 2014
"""

from mongoengine import StringField

from data_generation.model.state import State


class SBACState(State):
    """
    The SBAC-specific state class.
    """
    guid_sr = StringField(required=True)