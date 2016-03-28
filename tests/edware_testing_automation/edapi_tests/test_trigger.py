'''
Created on June 27, 2013

@author: nparoha
'''
import time

from sqlalchemy.sql import select

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.utils.db_connector import DBConnection
from edware_testing_automation.utils.db_utils import create_connection
from edware_testing_automation.utils.preferences import Edware
from edware_testing_automation.utils.preferences import preferences


class TestTrigger(ApiHelper):
    db_stat_url = None
    db_schema_name = None
    datasource_name = 'edware'
    build_guid = 'd2d02660-ddd7-11e2-a28f-0800200c9a66'
    insert_row = {'tenant': 'cat', 'load_type': 'assessment', 'load_start': 'now()', 'load_end': 'now()',
                  'load_status': 'ingested',
                  'batch_guid': build_guid, 'record_loaded_count': 1000, 'file_arrived': 'now()'}

    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)
        TestTrigger.db_stat_url = preferences(Edware.db_stats_main_url)
        TestTrigger.db_schema_name = preferences(Edware.db_stats_schema)
        create_connection(TestTrigger.db_stat_url, TestTrigger.db_schema_name,
                          datasource_name=TestTrigger.datasource_name)

    def setUp(self):
        self.check_table_in_schema("udl_stats")
        self.set_data_stat_table("udl_stats", TestTrigger.insert_row)
        self.check_table_not_empty("udl_stats")

    def tearDown(self):
        super(TestTrigger, self).tearDown()
        self.delete_stat_table("udl_stats")
        self.check_table_empty("udl_stats")

    def test_get_trigger_cache(self):
        self.set_request_cookie('gman')
        self.send_request("GET", "/services/trigger/cache")
        self.check_response_code(200)
        elements = self._response.json()
        self.assertEqual('OK', str(elements['result']), "Invalid response message")
        cache_trigger = self.select_pdf_cache_trigger_col_from_table("udl_stats", "last_pre_cached")
        self.assertIsNotNone(len(cache_trigger), 'Error: column "last_pre_cached" is empty')

    # @attr('pdf')
    def test_get_trigger_pdf(self):
        self.set_request_cookie('gman')
        self.send_request("GET", "/services/trigger/pdf")
        time.sleep(10)
        self.check_response_code(200)
        elements = self._response.json()
        self.assertEqual('OK', str(elements['result']), "Invalid response message")
        pdf_trigger = self.select_pdf_cache_trigger_col_from_table("udl_stats", "last_pdf_task_requested")
        self.assertIsNotNone(len(pdf_trigger), 'Error: column "last_pdf_task_requested" is empty')

    def test_get_cache_invalid_endpoint(self):
        self.set_request_cookie('gman')
        self.send_request("GET", "/services/trigger/cache123")
        self.check_response_code(404)

    # Send a request from a NON-super user id
    def test_get_cache_invalid_parameters(self):
        self.set_request_cookie('vlee')
        self.send_request("GET", "/services/trigger/cache")
        self.check_response_code(403)

    def test_get_pdf_invalid_endpoint(self):
        self.set_request_cookie('gman')
        self.send_request("GET", "/services/trigger/pdf123")
        self.check_response_code(404)

    # Send a request from a NON-super user id
    def test_get_pdf_invalid_parameters(self):
        self.set_request_cookie('vlee')
        self.send_request("GET", "/services/trigger/pdf")
        self.check_response_code(403)

    ###############################################################################################################
    ###  HELPER FUNCTIONS FOR CONSTRUCTING THE SQL QUERIES
    ###############################################################################################################

    # Find a specific table in the 'schema_name' schema
    def check_table_in_schema(self, table_name):
        found = False
        results = self.get_tables()
        for result in results:
            if table_name in result:
                found = True
                break
        self.assertTrue(found, 'Table {0} not found'.format(table_name))

    # query: select table_name from information_schema.tables where table_schema = schema_name;
    def get_tables(self):
        with DBConnection(name=TestTrigger.datasource_name) as connector:
            metadata = connector.get_metadata()
        return metadata.tables

    # Validate that the table is not empty
    def check_table_not_empty(self, table_name):
        results = self.select_from_table(table_name)
        self.assertIsNotNone(len(results), 'Error: Table {0} is empty'.format(table_name))

    # Validate that the table is empty
    def check_table_empty(self, table_name):
        results = self.select_from_table(table_name)
        self.assertEqual(len(results), 0, 'Error: Table {0} is not empty'.format(table_name))

    # query: select * from schema_name.table_name;
    def select_from_table(self, table):
        with DBConnection(name=TestTrigger.datasource_name) as connector:
            dim_table = connector.get_table(table)
            query = select([dim_table])
            results = connector.get_result(query)
        return results

    # query: select column_name from schema_name.table_name
    def select_pdf_cache_trigger_col_from_table(self, table, column_name):
        with DBConnection(name=TestTrigger.datasource_name) as connector:
            dim_table = connector.get_table(table)
            if column_name is "last_pre_cached":
                query = select([dim_table.c.last_pre_cached.label('last_pre_cached')])
            elif column_name is "last_pdf_task_requested":
                query = select([dim_table.c.last_pdf_task_requested.label('last_pdf_task_requested')])
            return connector.get_result(query)

    def delete_stat_table(self, table):
        with DBConnection(name=TestTrigger.datasource_name) as connector:
            table_name = connector.get_table(table)
            connector.execute(table_name.delete())

    # query: insert into schema_name.table_name (state_code,tenant,load_start,load_end,load_status,batch_guid,record_loaded_count)
    #        values('NC','cat',now(),now(),'ingested','cb28cf30-e024-11e2-a28f-0800200c9a66',1000);
    def set_data_stat_table(self, table, new_row):
        with DBConnection(name=TestTrigger.datasource_name) as connector:
            dim_table = connector.get_table(table)
            connector.execute(dim_table.insert().values(**new_row))
