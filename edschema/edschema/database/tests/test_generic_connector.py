'''
Created on Mar 4, 2013

@author: dip
'''
import unittest
from edschema.database.generic_connector import setup_db_connection_from_ini
from zope import component
from edschema.database.connector import IDbUtil, DBConnection


class TestGenericConnector(unittest.TestCase):

    def setUp(self):
        # Make sure we do not have sqlite in memory
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)
        self._settings = {'test.db.dummy.url': 'sqlite:///:memory:'}
        self._prefix = 'test.db.dummy.'
        self._metadata = None

    def tearDown(self):
        component.provideUtility(None, IDbUtil)

    def test_allow_create_is_false(self):
        setup_db_connection_from_ini(self._settings, self._prefix, self._metadata)
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNotNone(dbUtil)

    def test_create_with_engine_name(self):
        setup_db_connection_from_ini(self._settings, self._prefix, self._metadata, datasource_name='unitTest')
        dbUtil = component.queryUtility(IDbUtil, 'unitTest')
        self.assertIsNotNone(dbUtil)
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)

    def test_name_as_none(self):
        self.assertRaises(Exception, DBConnection, name=None)

if __name__ == "__main__":
    unittest.main()
