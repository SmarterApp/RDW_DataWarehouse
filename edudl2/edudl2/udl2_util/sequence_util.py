'''
Utility module to get global sequence from production database.
'''
from sqlalchemy import Sequence
from sqlalchemy.sql import select
from edudl2.database.udl2_connector import get_prod_connection
from sqlalchemy.schema import CreateSequence
from edudl2.udl2.celery import udl2_conf

INCREMENTAL = udl2_conf['prod_db']['global_seq_batch_size']

SEQUENCE_NAME = udl2_conf['prod_db']['global_seq_name']

PROD_SCHEMA_NAME = udl2_conf['prod_db']['db_schema']

START_WITH = 20 * 1000

class UDLSequence(object):
    '''
    UDL global sequence class.  The purpose of this class is to fetch
    and provide sequence in a central database for UDL, i.e. production
    database, in order to avoid primary key conflict duing migration
    when running multiple UDLs.
    '''

    def __init__(self, tenant_name, seq_name):
        self.tenant_name = tenant_name
        self.seq_name = seq_name
        self.max_value = -1
        self.current = 0
        self.check_sequence_existence()

    def fetch_next_batch(self):
        '''
        Gets sequence in batch.  Batch size is defined by
        `global_seq_batch_size` in configuration file.
        '''
        with get_prod_connection(self.tenant_name) as conn:
            seq = conn.execute("SELECT nextval('%s.%s') from generate_series(1, %d);"
                               % (PROD_SCHEMA_NAME, self.seq_name, INCREMENTAL))
            batch = [val[0] for val in seq]
            self.current = batch[0]
            self.max_value = batch[-1]

    def check_sequence_existence(self):
        '''
        Check if sequence exists, and create one if not.
        '''
        with get_prod_connection(self.tenant_name) as conn:
            if not self.sequence_exists(conn):
                seq = Sequence(name=self.seq_name, metadata=conn.get_metadata(), start=START_WITH)
                conn.execute(CreateSequence(seq))

    def sequence_exists(self, conn):
        '''
        Return True if sequence exists, otherwise return False.
        '''
        query = select([("sequence_name")]).select_from("information_schema.sequences")\
                                           .where("sequence_name = '" + self.seq_name + "'")
        exist = conn.execute(query).scalar()
        return exist

    def next(self):
        '''
        Get next sequence id.
        '''
        if self.current >= self.max_value + 1:
            self.fetch_next_batch()
        next_value = self.current
        self.current += 1
        return next_value


GLOBAL_SEQUENCE_POOL = {}


def get_global_sequence(tenant_name="edware"):
    '''
    TODO: add doc string
    '''
    if tenant_name in GLOBAL_SEQUENCE_POOL:
        return GLOBAL_SEQUENCE_POOL.get(tenant_name)
    seq = UDLSequence(tenant_name, SEQUENCE_NAME)
    GLOBAL_SEQUENCE_POOL[tenant_name] = seq
    return seq
