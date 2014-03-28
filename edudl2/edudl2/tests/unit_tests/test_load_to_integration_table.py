'''
Created on May 24, 2013

@author: ejen
'''
import unittest
import re
from edudl2.move_to_integration.move_to_integration import create_migration_query
from edcore.utils.utils import compile_query_to_sql_text
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.tests.functional_tests.util import UDLTestHelper


class TestLoadToIntegrationTable(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(TestLoadToIntegrationTable, cls).setUpClass()

    def test_create_migration_query(self):
        pass
