'''
Created on Feb 8, 2013

@author: tosako
'''
import unittest
from edschema.database.connector import DBConnection
from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
import types


class TestEdMetadata(Unittest_with_sqlite):

    # Test dim_district data
    def test_dim_inst_hier_type(self):
        self.assertTrue('dim_inst_hier' in self.get_Metadata().tables, "missing dim_inst_hier")
        with DBConnection() as connector:
            dim_inst_hier = connector.get_table("dim_inst_hier")

            # check number of field in the table
            self.assertEqual(12, len(dim_inst_hier.c), "Number of fields in dim_district")

            query = dim_inst_hier.select(dim_inst_hier.c.district_guid == '228')
            result = connector.get_result(query)
            self.assertEqual('228', result[0]['district_guid'])

    # Test get_stream_result with dim_district_data
    def test_get_streaming_result(self):
        self.assertTrue('dim_inst_hier' in self.get_Metadata().tables, "missing dim_inst_hier")
        with DBConnection() as connector:
            dim_inst_hier = connector.get_table("dim_inst_hier")

            # check number of field in the table
            self.assertEqual(12, len(dim_inst_hier.c), "Number of fields in dim_district")

            query = dim_inst_hier.select(dim_inst_hier.c.district_guid == '228')
            results = connector.get_streaming_result(query, fetch_size=1)
            self.assertEqual(type(results), types.GeneratorType)
            for result in results:
                self.assertEqual('228', result['district_guid'])
                break
            # test for larger file out of fetch_size
            fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
            query = fact_asmt_outcome.select()
            results = connector.get_streaming_result(query, fetch_size=1)
            self.assertEqual(type(results), types.GeneratorType)
            counter = 0
            for result in results:
                counter = counter + 1
            self.assertEqual(counter, 1275)

    # Test student_registration data
    def test_student_registration(self):
        self.assertTrue('student_reg' in self.get_Metadata().tables, "missing student_reg")
        with DBConnection() as connector:
            fact_student_reg = connector.get_table("student_reg")

            # Check number of fields in the table
            self.assertEqual(40, len(fact_student_reg.c), "Number of fields in student_registration")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
