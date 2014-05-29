__author__ = 'tshewchuk'
"""
This module describes the metadata schema for the HPZ database.
"""

from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, DateTime
from sqlalchemy import String
from hpz.database.constants import DatabaseConstants


def generate_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    file_registry = Table('file_registry', metadata,
                          Column(DatabaseConstants.REGISTRATION_ID, String(36), primary_key=True),
                          Column(DatabaseConstants.USER_ID, String(256), nullable=False),
                          Column(DatabaseConstants.FILE_PATH, String(256), nullable=True),
                          Column(DatabaseConstants.CREATE_DT, DateTime(timezone=True), nullable=True))

    return metadata
