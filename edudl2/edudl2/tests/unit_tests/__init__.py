import os
from edudl2.tests.utils.unittest import UDLTestCase


class UDLUnitTestCase(UDLTestCase):

    @classmethod
    def setUpClass(cls):
        # test source files
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        super().setUpClass(data_dir=data_dir)
