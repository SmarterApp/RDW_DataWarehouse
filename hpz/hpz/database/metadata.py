__author__ = 'tshewchuk'
"""
This module describes the metadata schema for the HPZ database.
"""

from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, DateTime
from sqlalchemy import String


def generate_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    file_registry = Table('file_registry', metadata,
                          Column('registration_id', String(36), primary_key=True),
                          Column('file_path', String(256), nullable=True),
                          Column('creation_date', DateTime(timezone=True), nullable=True))

    return metadata
