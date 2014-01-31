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

    def test_get_host_name_from_node_conn_info(self):
        conn_info = 'host=dbpgdw0.qa.dum.edwdc.net user=repmgr dbname=edware'
        self.assertEqual(queries.get_host_name_from_node_conn_info(conn_info), 'dbpgdw0.qa.dum.edwdc.net')
        conn_info = 'host=dbpgdw0.qa.dum.edwdc.net user=repmgr dbname=edware'
        self.assertEqual(queries.get_host_name_from_node_conn_info(conn_info), 'dbpgdw0.qa.dum.edwdc.net')


if __name__ == "__main__":
    unittest.main()
