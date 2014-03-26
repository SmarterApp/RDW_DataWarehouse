'''
Created on Mar 24, 2014

@author: agrebneva
'''
import unittest
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Index
from sqlalchemy import String, BigInteger
from edschema.metadata.util import get_natural_key, get_natural_key_columns


class TestMetadataUtil(unittest.TestCase):
    def setUp(self):
        self.__metadata = MetaData(schema='test_me', bind=False)
        test_table = Table('dim_inst_hier', self.__metadata,
                           Column('inst_hier_rec_id', BigInteger, primary_key=True),
                           Column('batch_guid', String(50), nullable=True),
                           Column('state_name', String(32), nullable=False),
                           Column('state_code', String(2), nullable=False),
                           Column('district_guid', String(50), nullable=False),
                           Column('district_name', String(256), nullable=False),
                           Column('school_guid', String(50), nullable=False),
                           Column('school_name', String(256), nullable=False),
                           Column('school_category', String(20), nullable=False),
                           )
        Index('dim_inst_hier_idx', test_table.c.inst_hier_rec_id, unique=True)
        Index('dim_inst_hier_codex', test_table.c.state_code, test_table.c.district_guid, test_table.c.school_guid, unique=False, natural_key=False)
        nkix = Index('dim_inst_hier_codex', test_table.c.state_code, test_table.c.district_guid, test_table.c.school_guid, unique=False, natural_key=True)
        self.__test_table = test_table
        self.__nkix = nkix

    def test_get_natural_key(self):
        '''
        test getting key if
        '''
        self.assertEquals(self.__nkix, get_natural_key(self.__test_table))

    def test_get_natural_key_with_dups(self):
        '''
        test getting one key if several natural_keys are detected
        '''
        nkix2 = Index('dim_inst_hier_codex2', self.__test_table.c.state_code, natural_key=True)
        self.assertTrue(get_natural_key(self.__test_table) in [self.__nkix, nkix2])

    def test_get_natural_key_columns(self):
        '''
        test get columns
        '''
        cols1 = get_natural_key_columns(self.__test_table)
        cols2 = self.__nkix.columns.keys()
        self.assertEquals(set(cols1), set(cols2))
