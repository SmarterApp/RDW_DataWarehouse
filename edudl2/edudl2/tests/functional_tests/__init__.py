import os
from edudl2.tests.utils.unittest import UDLTestCase
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf
from edudl2.database.udl2_connector import initialize_all_db


class UDLFunctionalTestCase(UDLTestCase):

    @classmethod
    def setUpClass(cls):
        # test source files
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        initialize_all_db(udl2_conf, udl2_flat_conf)
        super().setUpClass(data_dir=data_dir)
        cls.gpg_home = cls.settings.get('gpg_home')
