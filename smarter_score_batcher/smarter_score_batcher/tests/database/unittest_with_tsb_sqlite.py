from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from smarter_score_batcher.database.tsb_connector import config_namespace
from smarter_score_batcher.database.metadata import generate_tsb_metadata


class Unittest_with_tsb_sqlite(Unittest_with_sqlite):

    @classmethod
    def setUpClass(cls, force_foreign_keys=True):
        super().setUpClass(datasource_name=config_namespace, metadata=generate_tsb_metadata(), use_metadata_from_db=False, resources_dir=None, force_foreign_keys=force_foreign_keys)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
