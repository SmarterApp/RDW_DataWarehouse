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

"""
Created on Feb 13, 2013

@author: nparoha
"""
import allure

from edware_testing_automation.database_tests.database_helper import DatabaseTestHelper


@allure.feature('Third-party dependencies: postgres')
@allure.story('US12918: Data service - new schema and report refactoring')
class EdTestDatabase(DatabaseTestHelper):

    def __init__(self, *args, **kwargs):
        DatabaseTestHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        super(EdTestDatabase, self).setUp()

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
