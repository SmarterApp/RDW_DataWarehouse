'''
Created on Mar 24, 2014

@author: agrebneva
'''
import unittest
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Index, and_
from sqlalchemy import String, BigInteger, ForeignKey, SmallInteger
from edschema.metadata.util import *
from edschema.metadata.ed_metadata import MetaColumn


class TestMetadataUtil(unittest.TestCase):
    def setUp(self):
        self.__metadata = MetaData(schema='test_me', bind=False)
        test_dim_table = Table('dim_inst_hier', self.__metadata,
                               Column('inst_hier_rec_id', BigInteger, primary_key=True),
                               MetaColumn('batch_guid', String(50), nullable=True),
                               Column('state_name', String(32), nullable=False, info={'natural_key': True}),
                               Column('state_code', String(2), nullable=False),
                               Column('district_guid', String(50), nullable=False, info={'natural_key': True}),
                               Column('district_name', String(256), nullable=False),
                               Column('school_guid', String(50), nullable=False, info={'natural_key': True}),
                               Column('school_name', String(256), nullable=False),
                               Column('school_category', String(20), nullable=False),
                               MetaColumn('from_date', String(8), nullable=False),
                               MetaColumn('to_date', String(8), nullable=True),
                               MetaColumn('rec_status', String(1), nullable=False))
        Index('dim_inst_hier_idx', test_dim_table.c.inst_hier_rec_id, unique=True)
        Index('dim_inst_hier_codex', test_dim_table.c.state_code, test_dim_table.c.district_guid,
              test_dim_table.c.school_guid, unique=False)

        test_fact_table = Table('fact_asmt_outcome', self.__metadata,
                                Column('fact_asmt_outcome_rec_id', BigInteger, primary_key=True),
                                Column('inst_hier_rec_id', BigInteger, ForeignKey(test_dim_table.c.inst_hier_rec_id), nullable=False),
                                Column('asmt_grade', String(10), nullable=False),
                                Column('enrl_grade', String(10), nullable=False),
                                Column('date_taken', String(8), nullable=False),
                                Column('date_taken_day', SmallInteger, nullable=False),
                                Column('date_taken_month', SmallInteger, nullable=False),
                                Column('date_taken_year', SmallInteger, nullable=False),
                                Column('asmt_score', SmallInteger, nullable=False),
                                MetaColumn('batch_guid', String(50), nullable=True))

        self.__test_dim_table = test_dim_table
        self.__test_fact_table = test_fact_table
        self.__nkcol = [test_dim_table.c.state_name, test_dim_table.c.district_guid, test_dim_table.c.school_guid]
        self.__mkcol = [test_dim_table.c.batch_guid, test_dim_table.c.from_date, test_dim_table.c.to_date, test_dim_table.c.rec_status]
        self.__pkcol = [test_dim_table.c.inst_hier_rec_id]
        self.__test_fact_table_pkcol = [test_fact_table.c.fact_asmt_outcome_rec_id]
        self.__test_fact_table_mkcol = [test_fact_table.c.batch_guid]
        self.__test_fact_table_fkcol = [test_fact_table.c.inst_hier_rec_id]

    def test_get_natural_key(self):
        '''
        test getting key if
        '''
        self.assertEquals(self.__nkcol, get_natural_key(self.__test_dim_table))

    def test_get_natural_key_when_none_defined(self):
        '''
        test getting natural key if not defined
        '''
        test_table = Table('test_table', self.__metadata,
                           Column('student_rec_id', BigInteger, primary_key=True),
                           Column('batch_guid', String(50), nullable=True))
        self.assertTrue(len(get_natural_key(test_table)) == 0)

    def test_get_natural_key_columns(self):
        '''
        test get columns
        '''
        cols1 = get_natural_key_columns(self.__test_dim_table)
        cols2 = [c.name for c in self.__nkcol]
        self.assertEquals(set(cols1), set(cols2))

    def test_get_natural_key_columns_when_none_defined(self):
        '''
        test getting natural key columns if not defined
        '''
        test_table = Table('test_table', self.__metadata,
                           Column('student_rec_id', BigInteger, primary_key=True),
                           Column('batch_guid', String(50), nullable=True))
        self.assertTrue(len(get_natural_key_columns(test_table)) == 0)

    def test_get_foreign_key_columns_when_none_defined(self):
        '''
        test getting foreign key columns if none defined
        '''
        test_table = Table('test_table', self.__metadata,
                           Column('student_rec_id', BigInteger, primary_key=True),
                           Column('batch_guid', String(50), nullable=True))
        self.assertTrue(len(get_foreign_key_reference_columns(test_table)) == 0)

    def test_get_foreign_key_columns_one_defined(self):
        '''
        test getting foreign key columns if one defined
        '''
        test_table = Table('test_table', self.__metadata,
                           Column('student_rec_id', BigInteger, primary_key=True),
                           Column('enroll_inst_hier_rec_id', BigInteger, ForeignKey(self.__test_dim_table.c.inst_hier_rec_id), nullable=False),
                           Column('batch_guid', String(50), nullable=True))
        f_cols = get_foreign_key_reference_columns(test_table)
        self.assertTrue(len(f_cols) == 1)
        self.assertEquals(f_cols[0].name, 'enroll_inst_hier_rec_id')

    def test_get_foreign_key_columns_two_defined(self):
        '''
        test getting foreign key columns if two defined
        '''
        test_table = Table('test_table', self.__metadata,
                           Column('student_rec_id', BigInteger, primary_key=True),
                           Column('enroll_inst_hier_rec_id', BigInteger, ForeignKey(self.__test_dim_table.c.inst_hier_rec_id), nullable=False),
                           Column('asmt_inst_hier_rec_id', BigInteger, ForeignKey(self.__test_dim_table.c.inst_hier_rec_id), nullable=False),
                           Column('batch_guid', String(50), nullable=True))
        f_cols = get_foreign_key_reference_columns(test_table)
        self.assertTrue(len(f_cols) == 2)
        self.assertTrue(f_cols[0].name in ('enroll_inst_hier_rec_id', 'asmt_inst_hier_rec_id'))
        self.assertTrue(f_cols[1].name in ('enroll_inst_hier_rec_id', 'asmt_inst_hier_rec_id'))

    def test_get_meta_columns(self):
        '''
        test getting meta key columns
        '''
        self.assertEquals(self.__mkcol, get_meta_columns(self.__test_dim_table))

    def test_get_meta_columns_when_none_defined(self):
        '''
        test getting meta key columns if none defined
        '''
        test_table_none = Table('test_table', self.__metadata,
                                Column('student_rec_id', BigInteger, primary_key=True),
                                Column('batch_guid', String(50), nullable=True))
        self.assertTrue(len(get_meta_columns(test_table_none)) == 0)

    def test_get_primary_key_columns(self):
        '''
        test getting primary key columns
        '''
        self.assertEquals(self.__pkcol, get_primary_key_columns(self.__test_dim_table))

    def test_get_primary_key_columns_when_none_defined(self):
        '''
        test getting primary key columns if none defined
        '''
        test_table_none = Table('test_table', self.__metadata,
                                Column('student_rec_id', BigInteger),
                                Column('batch_guid', String(50), nullable=True))
        self.assertEquals(len(get_primary_key_columns(test_table_none)), 0)

    def test_get_matcher_key_columns(self):
        '''
        test getting matcher key columns
        '''
        expected_columns = set(self.__test_dim_table.columns) - set(self.__pkcol + self.__mkcol)
        self.assertEquals(expected_columns, set(get_matcher_key_columns(self.__test_dim_table)))

    def test_get_matcher_key_column_names(self):
        '''
        test getting matcher key column names
        '''
        expected_columns = set(self.__test_dim_table.columns) - set(self.__pkcol + self.__mkcol)
        expected_column_names = [c.name for c in expected_columns]
        self.assertEquals(expected_column_names, get_matcher_key_column_names(self.__test_dim_table))

    def test_get_tables_starting_with(self):
        '''
        test getting tables from metadata data using prefix of table name
        '''
        expected_tables = ['dim_inst_hier']
        self.assertEquals(expected_tables, get_tables_starting_with(self.__metadata, 'dim_'))

    def test_get_matcher_key_columns_for_fact(self):
        '''
        test getting matcher key columns for fact table
        '''
        expected_columns = set(self.__test_fact_table.columns) - set(self.__test_fact_table_pkcol +
                                                                     self.__test_fact_table_mkcol +
                                                                     self.__test_fact_table_fkcol)
        self.assertEquals(expected_columns, set(get_matcher_key_columns(self.__test_fact_table)))

    def test_get_selectable_by_table_name_for_single_table_query(self):
        '''
        test get selectable tables names from query
        '''
        query = Select([self.__test_fact_table.c.fact_asmt_outcome_rec_id,
                        self.__test_fact_table.c.inst_hier_rec_id], from_obj=self.__test_fact_table)
        self.assertEquals({'fact_asmt_outcome'}, set(get_selectable_by_table_name(query).values()))

    def test_get_selectable_by_table_name_for_multiple_table_join_query(self):
        '''
        test get selectable tables names from query
        '''
        query = Select([self.__test_fact_table.c.fact_asmt_outcome_rec_id,
                        self.__test_dim_table.c.inst_hier_rec_id],
                       from_obj=self.__test_fact_table.join(
                           self.__test_dim_table,
                           and_(self.__test_fact_table.c.inst_hier_rec_id == self.__test_dim_table.c.inst_hier_rec_id)))
        self.assertEquals({'fact_asmt_outcome', 'dim_inst_hier'}, set(get_selectable_by_table_name(query).values()))

    def test_get_selectable_by_table_name_for_multiple_table_join_query_with_alias(self):
        '''
        test get selectable tables names from query
        '''
        dim_alias = self.__test_dim_table.alias()
        fact_alias = self.__test_fact_table.alias()
        query = Select([self.__test_fact_table.c.fact_asmt_outcome_rec_id,
                        self.__test_dim_table.c.inst_hier_rec_id],
                       from_obj=fact_alias.join(dim_alias,
                           and_(self.__test_fact_table.c.inst_hier_rec_id == self.__test_dim_table.c.inst_hier_rec_id)))
        self.assertEquals({'fact_asmt_outcome', 'dim_inst_hier'}, set(get_selectable_by_table_name(query).values()))

    def test_get_selectable_by_table_name_for_multiple_table_join_query_with_named_alias(self):
        '''
        test get selectable tables names from query
        '''
        dim_alias = self.__test_dim_table.alias('dim_inst_hier_alias')
        fact_alias = self.__test_fact_table.alias('fact_asmt_outcome_alias')
        query = Select([self.__test_fact_table.c.fact_asmt_outcome_rec_id,
                        self.__test_dim_table.c.inst_hier_rec_id],
                       from_obj=fact_alias.join(
                           dim_alias,
                           and_(self.__test_fact_table.c.inst_hier_rec_id == self.__test_dim_table.c.inst_hier_rec_id)))
        self.assertEquals({'fact_asmt_outcome', 'dim_inst_hier'}, set(get_selectable_by_table_name(query).values()))

    def test_get_selectable_by_table_name_for_multi_table_join_with_query_tables(self):
        '''
        test get selectable tables names from query
        '''
        dim_alias = self.__test_dim_table.alias()
        fact_alias = self.__test_fact_table.alias()
        query = Select([self.__test_fact_table.c.fact_asmt_outcome_rec_id,
                        self.__test_dim_table.c.inst_hier_rec_id],
                       from_obj=fact_alias.join(dim_alias,
                           and_(self.__test_fact_table.c.inst_hier_rec_id == self.__test_dim_table.c.inst_hier_rec_id)))
        self.assertEquals({'fact_asmt_outcome', 'dim_inst_hier'}, set(get_selectable_by_table_name(query).values()))
