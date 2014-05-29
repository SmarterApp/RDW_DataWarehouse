__author__ = 'tshewchuk'
"""
This module describes the metadata schema for the HPZ database.
"""

from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, DateTime
from sqlalchemy import String
from hpz.database.constants import HPZ


def generate_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    file_registry = Table('file_registry', metadata,
                          Column(HPZ.REGISTRATION_ID, String(36), primary_key=True),
                          Column(HPZ.USER_ID, String(256), nullable=False),
                          Column(HPZ.FILE_PATH, String(256), nullable=True),
                          Column(HPZ.CREATE_DT, DateTime(timezone=True), nullable=True),
                          Column(HPZ.FILE_NAME, String(256), nullable=True))

    return metadata
