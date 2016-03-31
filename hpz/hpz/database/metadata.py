# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
                          Column(HPZ.EMAIL, String(256), nullable=True),
                          Column(HPZ.FILE_PATH, String(256), nullable=True),
                          Column(HPZ.CREATE_DT, DateTime(timezone=True), nullable=True),
                          Column(HPZ.FILE_NAME, String(256), nullable=True))

    return metadata
