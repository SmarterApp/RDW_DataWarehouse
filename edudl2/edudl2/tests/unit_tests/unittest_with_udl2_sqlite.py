'''
Created on Mar 28, 2014

@author: dip
'''
from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from edudl2.database.udl2_connector import TARGET_NAMESPACE,\
    PRODUCTION_NAMESPACE, UDL2DBConnection
from edschema.metadata.ed_metadata import generate_ed_metadata


class Unittest_with_udl2_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls, force_foreign_keys=True):
        super().setUpClass(datasource_name=TARGET_NAMESPACE + '.' + get_unittest_tenant_name(), metadata=generate_ed_metadata(), use_metadata_from_db=False,
                           resources_dir=None, force_foreign_keys=force_foreign_keys)
        super().setUpClass(datasource_name=PRODUCTION_NAMESPACE + '.' + get_unittest_tenant_name(), metadata=generate_ed_metadata(), use_metadata_from_db=False,
                           resources_dir=None, force_foreign_keys=force_foreign_keys)
        # TODO: for UDL, there's errors in create tables
        #super().setUpClass(datasource_name=UDL_NAMESPACE + '.' + get_unittest_tenant_name(), metadata=generate_udl2_metadata(), resources_dir=None,
        #                   force_foreign_keys=force_foreign_keys, import_data=False)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class UnittestUDLTargetDBConnection(UDL2DBConnection):
    def __init__(self):
        super().__init__(namespace=TARGET_NAMESPACE, tenant=get_unittest_tenant_name())


def get_unittest_tenant_name():
    return 'edware'


def get_unittest_schema_name():
    '''
    It's important that schema name is none for target connection as sqlite doesn't have concept of schema
    '''
    return None
