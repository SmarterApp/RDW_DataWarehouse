"""
Model the SBAC-specific items of a section.

@author: nestep
@date: March 14, 2014
"""

from mongoengine import IntField

from general.model.section import Section


class SBACSection(Section):
    """
    The SBAC-specific section class.
    """
    rec_id = IntField(required=True)