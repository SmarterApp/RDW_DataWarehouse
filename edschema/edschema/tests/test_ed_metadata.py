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

    def setUp(self):
        create_sqlite()
        generate_data()

    def tearDown(self):
        pass

    def test_tables(self):
        # get engine from zope
        dbUtil = component.queryUtility(IDbUtil)
        __engine = dbUtil.get_engine()

        # read metadata from database direclty instead of static metadata
        __metadata = MetaData()
        __metadata.reflect(bind=__engine)

        #check number of tables
        self.assertEqual(15, len(__metadata.tables), "Number of table does not match")
        """
        connector = DBConnector()
        dim_student = connector.get_table("dim_student1")
        self.assertIsNotNone(dim_student, "dim_student is missing")
        self.assertEqual("dim_student", dim_student.name, "msg")
        """
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
