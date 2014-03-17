"""
Generate IDs that conform to student registration (SBAC) requirements.

@author: nestep
@date: February 22, 2014
"""

from uuid import uuid4


def get_sr_uuid():
    """
    Get a UUID that conforms to student registration requirements.

    @returns: New UUID for student registration
    """
    return uuid4().hex[:30]
