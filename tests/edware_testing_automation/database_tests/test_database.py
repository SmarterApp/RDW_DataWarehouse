'''
Created on Feb 13, 2013

@author: nparoha
'''
from edware_testing_automation.database_tests.database_helper import DatabaseTestHelper


class EdTestDatabase(DatabaseTestHelper):
    def __init__(self, *args, **kwargs):
        DatabaseTestHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        super(EdTestDatabase, self).setUp()

    '''
    US12918: Data service - new schema and report refactoring
    '''

    def test_new_schema(self):
        print("TC_test_new_schema: Test new schema.")
        # Open a new connection and create a new cursor
        print("TC: Validate that a specific table is found in the schema.")
        self.check_table_in_schema("dim_asmt")
        self.check_table_in_schema("dim_inst_hier")
        self.check_table_in_schema("dim_student")
        self.check_table_in_schema("fact_asmt_outcome")
        self.check_table_in_schema("fact_asmt_outcome_vw")
        self.check_table_in_schema("fact_block_asmt_outcome")
        self.check_table_in_schema("student_reg")
        self.check_table_in_schema("custom_metadata")

        print("TC: Validate that a specific table is not empty.")
        self.check_table_not_empty("dim_asmt")
        self.check_table_not_empty("dim_inst_hier")
        self.check_table_not_empty("dim_student")
        self.check_table_not_empty("fact_asmt_outcome_vw")
        self.check_table_not_empty("fact_asmt_outcome")
        self.check_table_not_empty("fact_block_asmt_outcome")

    def tearDown(self):
        super(EdTestDatabase, self).tearDown()
