'''
Created on Feb 8, 2013

@author: tosako
'''
import unittest
from database.connector import DBConnector
from database.tests.unittest_with_sqlite import Unittest_with_sqlite


class Test(Unittest_with_sqlite):

    def test_number_of_tables(self):
        # check number of tables
        self.assertEqual(16, len(self.get_Metadata().tables), "Number of table does not match")

    # Test dim_district data
    def test_dim_district(self):
        self.assertTrue('dim_district' in self.get_Metadata().tables, "missing dim_district")
        connector = DBConnector()
        connector.open_connection()
        dim_district = connector.get_table("dim_district")

        # check number of field in the table
        self.assertEqual(7, len(dim_district.c), "Number of fields in dim_district")

        query = dim_district.select(dim_district.c.district_id == 1)
        result = connector.get_result(query)
        self.assertEqual(1, result[0]['district_id'], 'district_id')
        self.assertEqual("Daybreak District", result[0]['district_name'], "district_name")
        connector.close_connection()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
