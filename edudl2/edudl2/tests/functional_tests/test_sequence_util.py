import unittest
import uuid
from sqlalchemy import Sequence
from sqlalchemy.schema import DropSequence, CreateSequence
from edudl2.udl2_util.sequence_util import UDLSequence, get_global_sequence
from edudl2.database.udl2_connector import get_prod_connection, initialize_db_prod
from edudl2.tests.functional_tests.util import UDLTestHelper


class TestSequenceUtil(UDLTestHelper):

    def setUp(self):
        self.test_tenant = "cat"
        self.sequence_guid = str(uuid.uuid4())
        with get_prod_connection(self.test_tenant) as conn:
            seq = Sequence(name=self.sequence_guid, metadata=conn.get_metadata(), start=20000)
            conn.execute(CreateSequence(seq))

    @classmethod
    def setUpClass(cls):
        super(TestSequenceUtil, cls).setUpClass()
        initialize_db_prod(cls.udl2_conf)

    def tearDown(self,):
        with get_prod_connection(self.test_tenant) as conn:
            seq = Sequence(name=self.sequence_guid, metadata=conn.get_metadata())
            conn.execute(DropSequence(seq))

    def test_fetch_next_batch(self):
        seq = UDLSequence(tenant_name=self.test_tenant, seq_name=self.sequence_guid)
        seq.fetch_next_batch(batch_size=100)
        self.assertEqual(seq.current, 20000, "next batch should start from 20000")
        seq.fetch_next_batch(batch_size=200)
        self.assertEqual(seq.current, 20100, "next batch should start from 20100")
        seq.fetch_next_batch(batch_size=300)
        self.assertEqual(seq.current, 20300, "next batch should start from 20300")

    def test_sequence_existence(self):
        seq = UDLSequence(tenant_name=self.test_tenant, seq_name=self.sequence_guid)
        with get_prod_connection(self.test_tenant) as conn:
            seq_exist = seq.sequence_exists(conn)
            self.assertTrue(seq_exist, "sequence should exist already")

    def test_get_global_sequence(self):
        seq = get_global_sequence(self.test_tenant)
        sameSeq = get_global_sequence(self.test_tenant)
        self.assertEqual(seq, sameSeq, "Should return the same sequence")
        seq = get_global_sequence("nc")
        self.assertNotEqual(seq, sameSeq, "Should return different sequence")


if __name__ == '__main__':
    unittest.main()
