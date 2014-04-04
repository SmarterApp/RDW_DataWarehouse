'''
Created on Mar 24, 2014

@author: agrebneva
'''
import unittest
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Index
from sqlalchemy import String, BigInteger, ForeignKey
from edschema.metadata.util import get_natural_key, get_natural_key_columns, get_foreign_key_reference_columns


class TestMetadataUtil(unittest.TestCase):
    def setUp(self):
        self.__metadata = MetaData(schema='test_me', bind=False)
        test_table = Table('dim_inst_hier', self.__metadata,
                           Column('inst_hier_rec_id', BigInteger, primary_key=True),
                           Column('batch_guid', String(50), nullable=True),
                           Column('state_name', String(32), nullable=False, info={'natural_key': True}),
                           Column('state_code', String(2), nullable=False),
                           Column('district_guid', String(50), nullable=False, info={'natural_key': True}),
                           Column('district_name', String(256), nullable=False),
                           Column('school_guid', String(50), nullable=False, info={'natural_key': True}),
                           Column('school_name', String(256), nullable=False),
                           Column('school_category', String(20), nullable=False),
                           )
        Index('dim_inst_hier_idx', test_table.c.inst_hier_rec_id, unique=True)
        Index('dim_inst_hier_codex', test_table.c.state_code, test_table.c.district_guid,
              test_table.c.school_guid, unique=False)
        self.__test_table = test_table
        self.__nkcol = [test_table.c.state_name, test_table.c.district_guid, test_table.c.school_guid]

    def test_get_natural_key(self):
        '''
        test getting key if
        '''
        self.assertEquals(self.__nkcol, get_natural_key(self.__test_table))

    def test_get_natural_key_when_none_defined(self):
        '''
        test getting natural key if not defined
        '''
        test_table_none = Table('dim_student', self.__metadata,
                                Column('student_rec_id', BigInteger, primary_key=True),
                                Column('batch_guid', String(50), nullable=True))
        self.assertTrue(get_natural_key(test_table_none) is None)

    def test_get_natural_key_columns(self):
        '''
        test get columns
        '''
        cols1 = get_natural_key_columns(self.__test_table)
        cols2 = [c.name for c in self.__nkcol]
        self.assertEquals(set(cols1), set(cols2))

    def test_get_natural_key_columns_when_none_defined(self):
        '''
        test getting natural key columns if not defined
        '''
        test_table_none = Table('dim_student', self.__metadata,
                                Column('student_rec_id', BigInteger, primary_key=True),
                                Column('batch_guid', String(50), nullable=True))
        self.assertTrue(get_natural_key_columns(test_table_none) is None)

    def test_get_foreign_key_columns_when_none_defined(self):
        '''
        test getting foreign key columns if none defined
        '''
        test_table_none = Table('dim_student', self.__metadata,
                                Column('student_rec_id', BigInteger, primary_key=True),
                                Column('batch_guid', String(50), nullable=True))
        self.assertTrue(get_foreign_key_reference_columns(test_table_none) is None)

    def test_get_foreign_key_columns_one_defined(self):
        '''
        test getting foreign key columns if one defined
        '''
        test_table_one = Table('dim_student', self.__metadata,
                               Column('student_rec_id', BigInteger, primary_key=True),
                               Column('enroll_inst_hier_rec_id', BigInteger,
                                      ForeignKey(self.__test_table.c.inst_hier_rec_id), nullable=False),
                               Column('batch_guid', String(50), nullable=True))
        f_cols = get_foreign_key_reference_columns(test_table_one)
        self.assertTrue(len(f_cols) == 1)
        self.assertEquals(f_cols[0].name, 'enroll_inst_hier_rec_id')

    def test_get_foreign_key_columns_two_defined(self):
        '''
        test getting foreign key columns if two defined
        '''
        test_table_one = Table('dim_student', self.__metadata,
                               Column('student_rec_id', BigInteger, primary_key=True),
                               Column('enroll_inst_hier_rec_id', BigInteger,
                                      ForeignKey(self.__test_table.c.inst_hier_rec_id), nullable=False),
                               Column('asmt_inst_hier_rec_id', BigInteger,
                                      ForeignKey(self.__test_table.c.inst_hier_rec_id), nullable=False),
                               Column('batch_guid', String(50), nullable=True))
        f_cols = get_foreign_key_reference_columns(test_table_one)
        self.assertTrue(len(f_cols) == 2)
        self.assertTrue(f_cols[0].name in ('enroll_inst_hier_rec_id', 'asmt_inst_hier_rec_id'))
        self.assertTrue(f_cols[1].name in ('enroll_inst_hier_rec_id', 'asmt_inst_hier_rec_id'))
