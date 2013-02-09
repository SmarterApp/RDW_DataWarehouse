'''
Created on Feb 8, 2013

@author: tosako
'''
import unittest
from database.connector import DbUtil, IDbUtil, DBConnector
from zope import component
from sqlalchemy.schema import MetaData, Table
from database.tests.ed_sqlite import create_sqlite, generate_data


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite()
        # create test data in the sqlite
        generate_data()

        # get engine from zope
        dbUtil = component.queryUtility(IDbUtil)
        __engine = dbUtil.get_engine()
        # read metadata from database direclty instead of static metadata
        cls.__metadata = MetaData()
        cls.__metadata.reflect(bind=__engine)

    def test_number_of_tables(self):
        # check number of tables
        self.assertEqual(15, len(self.__metadata.tables), "Number of table does not match")

    # Test dim_district data
    def test_dim_district(self):
        self.assertTrue('dim_district' in self.__metadata.tables, "missing dim_district")
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
