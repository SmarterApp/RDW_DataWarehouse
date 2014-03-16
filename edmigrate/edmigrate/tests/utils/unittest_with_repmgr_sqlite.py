'''
Created on Mar 5, 2013

@author: tosako
'''
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite, \
    Unittest_with_sqlite_no_data_load

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles
import os
from edmigrate.tests.utils.repmgr_metadata import generate_repmgr_metadata
from edmigrate.database.repmgr_connector import RepMgrDBConnection


class Unittest_with_repmgr_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(__file__))
        metadata = generate_repmgr_metadata()
        resources_dir = os.path.abspath(os.path.join(os.path.join(here, '..', 'resources', 'repmgr')))
        super().setUpClass(RepMgrDBConnection.get_datasource_name(), metadata=metadata, resources_dir=resources_dir, use_metadata_from_db=False)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'
