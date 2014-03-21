'''
Created on Mar 17, 2014

@author: dip
'''
import unittest
from edschema.database.connector import DBConnection, IDbUtil, DbUtil
from zope import component


class DummyEngine():
    def __init__(self):
        pass

    def connect(self):
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
