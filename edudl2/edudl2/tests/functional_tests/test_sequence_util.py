import os
import unittest
import uuid
from sqlalchemy import Sequence
from sqlalchemy.schema import DropSequence
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.tests.unit_tests.unittest_with_udl2_sqlite import Unittest_with_udl2_sqlite,\
    UnittestUDLTargetDBConnection, get_unittest_schema_name,\
    get_unittest_tenant_name
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2_util.sequence_util import UDLSequence, get_global_sequence
from edudl2.database.udl2_connector import get_prod_connection, initialize_db_prod
from edudl2.tests.functional_tests.util import UDLTestHelper


class TestSequenceUtil(UDLTestHelper):

    def setUp(self):
        self.test_tenant = "edware"
        self.sequence_guid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        super(TestSequenceUtil, cls).setUpClass()
        initialize_db_prod(cls.udl2_conf)

    def tearDown(self,):
        #drop temporary sequence
        try:
            with get_prod_connection(self.test_tenant) as conn:
                seq = Sequence(name=self.sequence_guid, metadata=conn.get_metadata())
                conn.execute(DropSequence(seq))
        except:
            pass

    def test_next_id(self):
        seq = UDLSequence(tenant_name=self.test_tenant, seq_name=self.sequence_guid)
        for i in range(0, 2000):
            self.assertEqual(seq.next(), 20000 + i, "Should return next sequence id")

    def test_fetch_next_batch(self):
        seq = UDLSequence(tenant_name=self.test_tenant, seq_name=self.sequence_guid)
        seq.fetch_next_batch()
        self.assertEqual(seq.current, 20000, "next batch should start from 20100")
        self.assertEqual(seq.max_value, 20099, "next batch should end with 20200")
        seq.fetch_next_batch()
        self.assertEqual(seq.current, 20100, "next batch should start from 20100")
        self.assertEqual(seq.max_value, 20199, "next batch should end with 20200")

    def test_sequence_existence(self):
        seq = UDLSequence(tenant_name=self.test_tenant, seq_name=self.sequence_guid)
        with get_prod_connection(self.test_tenant) as conn:
            seq_exist = seq.sequence_exists(conn)
            self.assertTrue(seq_exist, "sequence should exist already")

    def test_get_global_sequence(self):
        seq = get_global_sequence(self.test_tenant)
        self.assertEqual(seq.next(), 20000, "Should return next sequence id")
        sameSeq = get_global_sequence(self.test_tenant)
        self.assertEqual(seq, sameSeq, "Should return the same sequence")
        self.assertEqual(sameSeq.next(), 20001, "Should return next sequence id")


if __name__ == '__main__':
    unittest.main()
