__author__ = 'tshewchuk'
"""
This module describes the metadata schema for the HPZ database.
"""

from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import String


def generate_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    file_registration = Table('file_registration', metadata,
                              Column('registration_id', String(36), primary_key=True))

    return metadata
