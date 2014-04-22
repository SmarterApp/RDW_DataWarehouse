from sqlalchemy import Sequence
from sqlalchemy.sql import select
from edudl2.database.udl2_connector import get_prod_connection
from sqlalchemy.schema import CreateSequence
from edudl2.udl2.celery import udl2_conf

INCREMENTAL = udl2_conf['prod_db']['global_seq_batch_size']

SEQUENCE_NAME = udl2_conf['prod_db']['global_seq_name']

SCHEMA_NAME = udl2_conf['prod_db']['db_schema']


class UDLSequence:

    def __init__(self):
        self.max_value = -1
        self.current = 0
        self.check_sequence_existence()

    def fetch_next_batch(self):
        with get_prod_connection() as conn:
            seq = conn.execute("SELECT nextval('%s.%s') from generate_series(1, %d);"
                               % (SCHEMA_NAME, SEQUENCE_NAME, INCREMENTAL))
            batch = [val[0] for val in seq]
            self.current = batch[0]
            self.max_value = batch[-1]

    def check_sequence_existence(self):
        with get_prod_connection() as conn:
            if not self.sequence_exists(conn):
                seq = Sequence(name=SEQUENCE_NAME, metadata=conn.get_metadata(), start=20 * 1000)
                conn.execute(CreateSequence(seq))

    def sequence_exists(self, conn):
        query = select([("sequence_name")]).select_from("information_schema.sequences")\
                                           .where("sequence_name = '" + SEQUENCE_NAME + "'")
        exist = conn.execute(query).scalar()
        return exist

    def next(self):
        if self.current >= self.max_value + 1:
            self.fetch_next_batch()
        next_value = self.current
        self.current += 1
        return next_value


GLOBAL_SEQUENCE = UDLSequence()
