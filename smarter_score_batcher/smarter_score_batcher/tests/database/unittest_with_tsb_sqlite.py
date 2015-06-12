from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from smarter_score_batcher.database.tsb_connector import config_namespace,\
    TSBDBConnection
from smarter_score_batcher.database.metadata import generate_tsb_metadata
from smarter_score_batcher.constant import Constants


class Unittest_with_tsb_sqlite(Unittest_with_sqlite):

    @classmethod
    def setUpClass(cls, force_foreign_keys=False):
        super().setUpClass(datasource_name=config_namespace, metadata=generate_tsb_metadata(), use_metadata_from_db=False, resources_dir=None, force_foreign_keys=force_foreign_keys)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def tearDown(self):
        with TSBDBConnection() as conn:
            conn.execute(conn.get_table(Constants.TSB_ASMT).delete())
            conn.execute(conn.get_table(Constants.TSB_METADATA).delete())
            conn.execute(conn.get_table(Constants.TSB_ERROR).delete())
