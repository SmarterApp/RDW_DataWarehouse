__author__ = 'sravi'

import unittest
import edmigrate.utils.queries as queries


# TODO: Create a test util base class with test data for repl_mgr schema and tables and inherit that
class TestQueries(unittest.TestCase):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        pass

    def test_get_slave_node_ids_from_host_name(self):
        slave_host_names = ['testslave0.qa.dum.edwdc.net', 'testslave1.qa.dum.edwdc.net']
        queries.get_slave_node_ids_from_host_name('repmgr', slave_host_names)


if __name__ == "__main__":
    unittest.main()
