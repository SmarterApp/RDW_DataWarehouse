'''
Created on Mar 2, 2013

@author: tosako
'''
from sqlalchemy.schema import MetaData, Table, Column
from sqlalchemy.types import SMALLINT, String, Integer, Boolean


def generate_test_metadata(scheme_name=None, bind=None):

    metadata = MetaData(schema=scheme_name, bind=bind)

    table_a = Table('table_a', metadata,
                    Column('row_int_primary', SMALLINT, primary_key=True),
                    Column('row_int', Integer, nullable=False),
                    Column('row_string_5', String(5), nullable=True),
                    )
    table_b = Table('table_b', metadata,
                    Column('row_int_primary', SMALLINT, primary_key=True),
                    Column('row_int', Integer, nullable=False),
                    Column('updated', Boolean, nullable=True),
                    )
    return metadata
