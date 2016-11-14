'''
Created on Aug 28, 2013

@author: bpatel
'''
import unittest
import os
import csv
import subprocess
from sqlalchemy import create_engine, MetaData

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

EDSCHEMA_PATH = os.path.join(__location__, '..', '..', '..', 'edschema', 'edschema', 'metadata_generator.py')
components = __location__.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])
ENTITY_TO_PATH_DICT = {'dim_inst_hier': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_inst_hier.csv'),
                       'dim_section': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_section.csv'),
                       'dim_asmt': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_asmt.csv'),
                       'fact_asmt_outcome': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                       'external_user_student_rel': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'external_user_student_rel.csv'),
                       'dim_student': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_student.csv')}


class ColumnValidationFuncTest(unittest.TestCase):

    def setUp(self):
        self.schema_name = 'edware_column_validation_functional_tests'
        self.database_name = 'data_generation_functional_tests'
        self.host = 'edwdbsrv2.poc.dum.edwdc.net'
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.port = 5432

        create_edware_schema(self.schema_name, self.database_name, self.host, self.user, self.passwd)

    def tearDown(self):
        delete_edware_schema(self.schema_name, self.database_name, self.host, self.user, self.passwd)

    def test_columns_match(self):
        csv_columns = self.get_headers_from_csv()
        database_columns = self.get_headers_from_database()
        print(csv_columns.keys())
        print(database_columns.keys())

        for table in csv_columns:
            self.assertEqual(len(csv_columns[table]), len(database_columns[table]), "columns don't match for table: %s" % table)
            self.assertSetEqual(set(csv_columns[table]), set(database_columns[table]))

    def get_headers_from_csv(self):
        '''
        Open each csv file and pull out the first row
        '''
        headers = {}
        for entity in ENTITY_TO_PATH_DICT:
            with open(ENTITY_TO_PATH_DICT[entity], "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                headers[entity] = next(csv_reader)
        return headers

    def get_headers_from_database(self):
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'
        db_string = db_string.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database_name)
        engine = create_engine(db_string)
        metadata = MetaData()
        metadata.reflect(engine, self.schema_name)

        table_columns = {}
        for table in metadata.sorted_tables:
            table_columns[table.name] = [x.name for x in table.columns]

        return table_columns


def create_edware_schema(schema_name, database, host, user, passwd):
    output = system('python', EDSCHEMA_PATH, '-s', schema_name, '-d', database, '--host', host, '-u', user, '-p', passwd, '-m', 'edware')
    print(output.decode('UTF-8'))


def delete_edware_schema(schema_name, database, host, user, passwd):
    output = system('python', EDSCHEMA_PATH, '-s', schema_name, '-d', database, '--host', host, '-u', user, '-p', passwd, '-m', 'edware', '--action', 'teardown')
    print(output.decode('UTF-8'))


def system(*args, **kwargs):
    '''
    Method for running system calls
    Taken from the pre-commit file for python3 in the scripts directory
    '''
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _err = proc.communicate()
    return out


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
