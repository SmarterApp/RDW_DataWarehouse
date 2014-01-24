'''
Created on Mar 8, 2013

@author: tosako
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite_no_data_load,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.reports.compare_pop_report import QueryHelper,\
    set_default_min_cell_size
from smarter.reports.helpers.constants import Constants
from smarter.reports.exceptions.parameter_exception import InvalidParameterException
from edauth.security.session import Session
from pyramid import testing
from pyramid.testing import DummyRequest
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.constants import RolesConstants


class Test(Unittest_with_edcore_sqlite_no_data_load):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
        dummy_session = Session()
        dummy_session.set_roles([RolesConstants.STATE_EDUCATION_ADMINISTRATOR_1])
        dummy_session.set_uid('272')
        dummy_session.set_tenants([get_unittest_tenant_name()])
        self.__config.testing_securitypolicy(dummy_session)
        set_default_min_cell_size(0)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_build_columns_state_view(self):
        with UnittestEdcoreDBConnection() as connection:
            helper = QueryHelper(connection, **get_param_state_view())
            query = helper.get_query_for_state_view()
            columns = query._raw_columns
            dim_inst_hier = connection.get_table(Constants.DIM_INST_HIER)

        self.assertEquals(5, len(columns))
        # first three columns are for state view columns
        # test alias name
        self.assertEqual(columns[0].name, Constants.NAME, 'test for alias name')
        self.assertEqual(columns[0].element.table.name, dim_inst_hier.name)
        self.assertEqual(columns[0].element.name, dim_inst_hier.c.district_name.name)
        self.assertEqual(columns[1].name, Constants.ID, 'test for alias name')
        self.assertEqual(columns[1].element.table.name, dim_inst_hier.name)
        self.assertEqual(columns[1].element.name, dim_inst_hier.c.district_guid.name)
        self.assertEqual(columns[2].name, Constants.ASMT_SUBJECT, 'test for alias name')

    def test_build_columns_district_view(self):
        with UnittestEdcoreDBConnection() as connection:
            helper = QueryHelper(connection, **get_param_district_view())
            query = helper.get_query_for_district_view()
            columns = query._raw_columns
            dim_inst_hier = connection.get_table(Constants.DIM_INST_HIER)

        self.assertEquals(5, len(columns))

        # first three columns are for district view columns
        # test alias name
        self.assertEqual(columns[0].name, Constants.NAME, 'test for alias name')
        self.assertEqual(columns[0].element.table.name, dim_inst_hier.name)
        self.assertEqual(columns[0].element.name, dim_inst_hier.c.school_name.name)
        self.assertEqual(columns[1].name, Constants.ID, 'test for alias name')
        self.assertEqual(columns[1].element.table.name, dim_inst_hier.name)
        self.assertEqual(columns[1].element.name, dim_inst_hier.c.school_guid.name)
        self.assertEqual(columns[2].name, Constants.ASMT_SUBJECT, 'test for alias name')

    def test_build_columns_school_view(self):
        with UnittestEdcoreDBConnection() as connection:
            helper = QueryHelper(connection, **get_param_school_view())
            query = helper.get_query_for_school_view()
            columns = query._raw_columns
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)

        self.assertEquals(5, len(columns))
        # first two columns are for school view columns
        # test alias name
        self.assertEqual(columns[0].name, Constants.NAME, 'test for alias name')
        self.assertEqual(columns[1].name, Constants.ID, 'test for alias name')
        self.assertEqual(columns[1].element.table.name, fact_asmt_outcome.name)
        self.assertEqual(columns[1].element.name, fact_asmt_outcome.c.asmt_grade.name)
        self.assertEqual(columns[2].name, Constants.ASMT_SUBJECT, 'test for alias name')

    def check_asmt_custom_metadata(self, connection, asmt_custom_metadata_column):
        self.assertEqual(asmt_custom_metadata_column.name, Constants.ASMT_CUSTOM_METADATA)
        # reuse when asmt_custom_metadata is moved to its table
        #dim_asmt = connection.get_table(Constants.DIM_ASMT)
        #self.assertEqual(asmt_custom_metadata_column.element.table.name, dim_asmt.name)
        #self.assertEqual(asmt_custom_metadata_column.element.name, dim_asmt.c.asmt_custom_metadata.name)

    def check_performance_level_column(self, column, alias_name):
        self.assertEqual(column.key, alias_name)

    def test_invalid_parameters(self):
        param = {'stateCode': 'DE', 'schoolGuid': 'BAC'}
        self.assertRaises(InvalidParameterException, QueryHelper, None, **param)


def get_param_school_view():
    return {Constants.STATECODE: 'AB', Constants.DISTRICTGUID: 'CD', Constants.SCHOOLGUID: 'EF'}


def get_param_district_view():
    return {Constants.STATECODE: 'AB', Constants.DISTRICTGUID: 'CD'}


def get_param_state_view():
    return {Constants.STATECODE: 'AB'}


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
