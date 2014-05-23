'''
Utility module to get global sequence from production database.
'''
from celery.utils.log import get_task_logger
from sqlalchemy.sql import select
from edudl2.database.udl2_connector import get_prod_connection
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2.constants import Constants
from edudl2.udl2_util.exceptions import UDL2GlobalSequenceMissingException

logger = get_task_logger(__name__)

# size of each sequence batch
INCREMENTAL = udl2_conf['global_sequence']['batch_size']

# sequence start number, to avoid key conflict in first batch
START_WITH = udl2_conf['global_sequence']['start_with']


class UDLSequence(object):
    '''
    UDL global sequence class.  The purpose of this class is to fetch
    and provide sequence in a central database for UDL, i.e. production
    database, in order to avoid primary key conflict duing migration
    when running multiple UDLs.
    '''

    def __init__(self, tenant_name, seq_name):
        self.tenant_name = tenant_name
        self.schema_name = udl2_conf['prod_db_conn'][tenant_name]['db_schema']
        self.seq_name = seq_name
        self.current = 0
        self.check_sequence_existence()

    def check_sequence_existence(self):
        '''
        Check if sequence exists, if not raise exception UDL2GlobalSequenceMissingExceptin
        '''
        with get_prod_connection(self.tenant_name) as conn:
                if not self.sequence_exists(conn):
                    raise UDL2GlobalSequenceMissingException(
                        msg='UDL2 Prod Global Sequence Missing for tenant: ' + self.tenant_name)

    def sequence_exists(self, conn):
        '''
        Return True if sequence exists, otherwise return False.
        '''
        query = select([("sequence_name")]).select_from("information_schema.sequences")\
                                           .where("sequence_name = '" + self.seq_name + "'")
        exist = conn.execute(query).scalar()
        return exist

    def fetch_next_batch(self, batch_size):
        '''
        Gets sequence in batch.  Batch size is defined by
        `global_seq_batch_size` in configuration file.
        '''
        with get_prod_connection(self.tenant_name) as conn:
            seq = conn.execute("SELECT nextval('%s.%s') from generate_series(1, %d);"
                               % (self.schema_name, self.seq_name, batch_size))
            batch = seq.fetchone()
            self.current = batch[0]
            seq.close()

    def offset(self, batch_size):
        '''
        '''
        self.fetch_next_batch(batch_size)
        return self.current


GLOBAL_SEQUENCE_POOL = {}


def get_global_sequence(tenant_name):
    '''
    Get global sequence for given tenant.
    '''
    #import pdb;pdb.set_trace()
    if tenant_name in GLOBAL_SEQUENCE_POOL:
        return GLOBAL_SEQUENCE_POOL.get(tenant_name)
    seq = UDLSequence(tenant_name, Constants.SEQUENCE_NAME)
    GLOBAL_SEQUENCE_POOL[tenant_name] = seq
    return seq
