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
