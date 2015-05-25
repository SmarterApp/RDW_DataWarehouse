from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from hpz.database.metadata import generate_metadata
from hpz.database.hpz_connector import HPZ_NAMESPACE


class Unittest_with_hpz_sqlite(Unittest_with_sqlite):

    @classmethod
    def setUpClass(cls, force_foreign_keys=True):
        super().setUpClass(datasource_name=HPZ_NAMESPACE, metadata=generate_metadata())

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
