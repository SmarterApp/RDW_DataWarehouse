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

'''
Created on Mar 17, 2014

@author: dip
'''
import unittest
from edschema.database.connector import DBConnection, IDbUtil, DbUtil
from zope import component
from sqlalchemy.exc import DatabaseError


class DummyEngine():
    def __init__(self):
        pass

    def connect(self):
        return DummyConn()


class DummyConn():
    def execution_options(self, stream_results):
        return self

    @staticmethod
    def execute(statement, *kwargs, **args):
        raise DatabaseError(statement, kwargs, args, connection_invalidated=True)

    def close(self):
        pass


class DummyMetadata():
    def __init__(self):
        pass


def dummyFunc(**kwargs):
    return 'testingDummyFunc'


class TestConnector(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        component.provideUtility(None, IDbUtil)

    def test_get_engine(self):
        dbUtil = DbUtil(engine=DummyEngine(), metadata=DummyMetadata())
        component.provideUtility(dbUtil, IDbUtil, name='unittest')
        db = DBConnection('unittest')
        self.assertIsInstance(db.get_engine(), DummyEngine)

    def test_get_metadata(self):
        dbUtil = DbUtil(engine=DummyEngine(), metadata=DummyMetadata())
        component.provideUtility(dbUtil, IDbUtil, name='unittest')
        db = DBConnection('unittest')
        self.assertIsInstance(db.get_metadata(), DummyMetadata)

    def test_set_metadata_by_generate(self):
        dbUtil = DbUtil(engine=DummyEngine(), metadata=DummyMetadata())
        component.provideUtility(dbUtil, IDbUtil, name='unittest')
        db = DBConnection('unittest')
        db.set_metadata_by_generate('schema_name', dummyFunc)
        metadata = db.get_metadata()
        self.assertEqual(metadata, dummyFunc())

    def test_retries(self):
        dbUtil = DbUtil(engine=DummyEngine(), metadata=DummyMetadata())
        component.provideUtility(dbUtil, IDbUtil, name='unittest')
        db = DBConnection('unittest')
        self.assertRaises(DatabaseError, db.execute, 'query')


if __name__ == "__main__":
    unittest.main()
