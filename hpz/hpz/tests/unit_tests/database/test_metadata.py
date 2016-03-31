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
Unit tests for the metadata schema module for the HPZ database.
"""

import unittest

from sqlalchemy.engine import create_engine

from hpz.database.metadata import generate_metadata


class TestMetadata(unittest.TestCase):

    def test_generate_metadata(self):
        engine = create_engine('postgresql+pypostgresql://my_bind')
        metadata = generate_metadata(schema_name='my_schema', bind=engine)
        self.assertEqual('my_schema', metadata.schema)
        self.assertIs(engine, metadata.bind)
