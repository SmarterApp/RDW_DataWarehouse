'''
Created on Mar 12, 2013

@author: igill
'''
from backend_tests.testbase import TestBase
from sqlalchemy.engine import create_engine
from sqlalchemy import event
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table
from sqlalchemy.schema import Column
from sqlalchemy import String, Integer, Float, SmallInteger, Unicode, Date, DateTime
from sqlalchemy import ForeignKey
from edschema.metadata.ed_metadata import generate_ed_metadata
from sqlalchemy.types import NULLTYPE, FLOAT, UnicodeText
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
import datetime


class EdTestSchema(TestBase):

    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)
        self.db_url = self.get_db_url('edware')
        self.db_schema = self.get_schema_name('edware')
        self.qa_db_url = self.get_db_url('edware', mode='qa')
        self.qa_db_schema = self.get_schema_name('edware', mode='qa')

    def setUp(self):
        super(TestBase, self).setUp()
        self.pgengine = create_engine(self.db_url)
        self.connection = self.pgengine.connect()
        #retrieving schema information (as Metadata) from live database
        self.live_db_metadata = MetaData(schema=self.db_schema)
        self.live_db_metadata.reflect(bind=self.pgengine)
        #retrieving Metadata information from edmetadata.py prior to db creation (to ensure live metadata matches expected metadata)
        self.ed_metadata = generate_ed_metadata(schema_name=self.get_schema_name('edware'))
        self.create_mismatch_schema()

    #in each table in the live db, if a column has a foreign key, check the data type matches primary column
    #added qa_test variable to allow switching from default 'edware' database to one that has bad data to confirm the test works
    def test_foreign_key_datatypes(self, qa_test=None):
        if qa_test:
            qa_engine = create_engine(self.qa_db_url)
            connection = qa_engine.connect()
            live_metadata = MetaData(schema=self.qa_db_schema)
            live_metadata.reflect(bind=qa_engine)
        else:
            live_metadata = self.live_db_metadata
        for table in live_metadata.tables:
            for column in live_metadata.tables[table].columns.keys():
                if len(list(live_metadata.tables[table].columns[column].foreign_keys)) > 0:
                    try:
                        #when running using nosetests, print statements will not be displayed unless there is a test failure or nose is set to verbose
                        print('Primary key is:' + str(live_metadata.tables[table].columns[column].type))
                        print('Foreign key is:' + str(list(live_metadata.tables[table].columns[column].foreign_keys)[0].column.type))
                        assert str(live_metadata.tables[table].columns[column].type) == str(list(live_metadata.tables[table].columns[column].foreign_keys)[0].column.type), "Foreign key mismatch"
                    except AssertionError as e:
                        #normal test should pass
                        if not qa_test:
                            raise AssertionError(e)
                    else:
                        #all qa_test should fail
                        if qa_test:
                            raise AssertionError('Failure expected!')

    #check that the ed_metadata matches the live metadata in tables,columns, and datatypes
    def test_live_metadata_to_ed_metadata(self):
        for table in self.live_db_metadata.tables:
            assert table in self.ed_metadata.tables, "Unexpected table in live db"
            for column in self.live_db_metadata.tables[table].columns.keys():
                assert column in self.ed_metadata.tables[table].columns.keys(), "Unexpected column in live db"

                if str(self.ed_metadata.tables[table].columns[column].type) == 'FLOAT':
                    #need to do a manual comparison of FLOAT (SQLAlchemy type) and DOUBLE PRECISION(Postgres type)
                    assert str(self.live_db_metadata.tables[table].columns[column].type) == 'DOUBLE PRECISION'
                elif self.ed_metadata.tables[table].columns[column].type.python_type is datetime.datetime:
                    assert str(self.live_db_metadata.tables[table].columns[column].type) == 'TIMESTAMP WITHOUT TIME ZONE'
                else:
                    #All other SQLAlchemy and equivalent Postgres types comparisons can be done with string casting
                    assert str(self.live_db_metadata.tables[table].columns[column].type) == str(self.ed_metadata.tables[table].columns[column].type), "Column datatype mismatch"

    def test_with_bad_schema(self):
        self.test_foreign_key_datatypes(True)

    def tearDown(self):
        self.pgengine.dispose()
        self.destroy_mismatch_schema()

    def _generate_mismatch_metadata(self, engine, schema):
        qa_metadata = MetaData(bind=engine, schema=schema)
        # Here, we intentionally generated mismatched foreign keys among a sets of tables.
        # So we can Meta Test tests above
        # Please refer https://confluence.wgenhq.net/display/CS/Postgres+Schema+Rules for all cases

        tbl_string = Table('tbl_string', qa_metadata, Column('id', String(50), primary_key=True), schema=schema,)
        tbl_unicode = Table('tbl_unicode', qa_metadata, Column('id', UnicodeText, primary_key=True), schema=schema,)
        tbl_date = Table('tbl_date', qa_metadata, Column('id', Date, primary_key=True), schema=schema,)
        tbl_datetime = Table('tbl_datetime', qa_metadata, Column('id', DateTime, primary_key=True), schema=schema,)
        tbl_integer = Table('tbl_integer', qa_metadata, Column('id', Integer, primary_key=True), schema=schema,)
        tbl_small_integer = Table('tbl_small_integer', qa_metadata, Column('id', SmallInteger, primary_key=True), schema=schema,)
        tbl_float = Table('tbl_float', qa_metadata, Column('id', Float, primary_key=True), schema=schema,)
        tbl_master = Table('tbl_master', qa_metadata,
                           Column('id', Integer, primary_key=True),
                           Column('string_short', String(5), ForeignKey(tbl_string.c.id)),
                           Column('string_long', String(100), ForeignKey(tbl_string.c.id)),
                           Column('unicode_string', UnicodeText, ForeignKey(tbl_string.c.id)),
                           Column('string_unicode', String(50), ForeignKey(tbl_unicode.c.id)),
                           Column('datetime_date', DateTime, ForeignKey(tbl_date.c.id)),
                           Column('date_datetime', Date, ForeignKey(tbl_datetime.c.id)),
                           Column('small_integer_integer', SmallInteger, ForeignKey(tbl_integer.c.id)),
                           Column('integer_small_integer', Integer, ForeignKey(tbl_small_integer.c.id)),
                           Column('integer_float', Integer, ForeignKey(tbl_float.c.id)),
                           schema=schema)
        return qa_metadata

    def create_mismatch_schema(self):
        pgengine = create_engine(self.qa_db_url)
        connection = pgengine.connect()
        trans = connection.begin()
        qa_metadata = self._generate_mismatch_metadata(pgengine, self.qa_db_schema)
        try:
            qa_metadata.create_all()
        finally:
            trans.commit()
            connection.close()

    def destroy_mismatch_schema(self):
        # I can't use SQLAlchemy's metadata.drop_all to drop tables correctly due to drop cascade.
        # I found this on google and tested it. http://www.executionunit.com/en/blog/2007/11/23/postgresql-sqlalchemy-dropping-all-tables-and-sequences/
        pgengine = create_engine(self.qa_db_url)
        qa_metadata = MetaData(bind=pgengine, schema=self.qa_db_schema)
        #qa_metadata.drop_all()
        connection = pgengine.connect()
        trans = connection.begin()
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='" + self.qa_db_schema + "'"
        tables = connection.execute(sql)
        for (table,) in tables:
            try:
                connection.execute("DROP TABLE %s CASCADE" % (self.qa_db_schema + '.' + table))
            except Exception as e:
                print(e)
        sql = "SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema='" + self.qa_db_schema + "'"
        seqs = connection.execute(sql)
        for (seq,) in seqs:
            try:
                connection.execute("DROP SEQUENCE %s CASCADE" % (self.qa_db_schema + '.' + seq))
            except Exception as e:
                print(e)
        trans.commit()
        connection.close()
