'''
Created on Mar 12, 2013

@author: igill
'''
from testbase import TestBase
from sqlalchemy.engine import create_engine
from sqlalchemy import event
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table
from edschema.ed_metadata import generate_ed_metadata
from sqlalchemy.types import NULLTYPE

class EdTestSchema(TestBase):

    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)
        self.db_url = self.get_db_url('edware')
        self.db_schema=self.get_schema_name('edware')
        
    def setUp(self):
        super(TestBase, self).setUp()
        self.pgengine = create_engine(self.db_url)
        self.connection = self.pgengine.connect()
        self.live_db_metadata = MetaData(schema=self.db_schema)
        self.live_db_metadata.reflect(bind=self.pgengine)
        self.ed_metadata = generate_ed_metadata(schema_name=self.get_schema_name('edware'))
 
    #in each table in the live db, if a column has a foreign key, check the data type matches primary column
    def test_foreign_key_datatypes(self):
        for table in self.live_db_metadata.tables:
            for column in self.live_db_metadata.tables[table].columns.keys():
                if len(list(self.live_db_metadata.tables[table].columns[column].foreign_keys)) > 0:
                    assert str(self.live_db_metadata.tables[table].columns[column].type) == str(list(self.live_db_metadata.tables[table].columns[column].foreign_keys)[0].column.type)
    
    #check that the ed_metadata matches the live metadata in tables,columns, and datatypes
    def test_live_metadata_to_ed_metadata(self):
        for table in self.live_db_metadata.tables:
            assert table in self.ed_metadata.tables, "Unexpected table in live db"
            for column in self.live_db_metadata.tables[table].columns.keys():
                assert column in self.ed_metadata.tables[table].columns.keys(), "Unexpected column in live db"
                assert str(self.live_db_metadata.tables[table].columns[column].type) == str(self.ed_metadata.tables[table].columns[column].type), "Column datatype mismatch"
               
    def tearDown(self):
        self.pgengine.dispose()