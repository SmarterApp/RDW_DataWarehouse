"""
Model a registration system for the SBAC project.

@author: nestep
@date: March 4, 2014
"""

from mongoengine import DateTimeField, Document, IntField, StringField


class SBACRegistrationSystem(Document):
    """
    Model a SBAC registration system.
    """
    guid = StringField(required=True, primary_key=True)
    sys_guid = StringField(required=True)
    academic_year = IntField(required=True)
    extract_date = DateTimeField(required=True)
    callback_url = StringField(required=True)

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'registration_system': self}
