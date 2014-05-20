__author__ = 'tshewchuk'
"""
This module describes the metadata schema for the HPZ database.
"""

from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Date
from sqlalchemy import String


def generate_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    file_registry = Table('file_registry', metadata,
                          Column('uuid', String(36), primary_key=True),
                          Column('file_path', String(256), nullable=True),
                          Column('creation_date', Date(), nullable=True),)

    return metadata
