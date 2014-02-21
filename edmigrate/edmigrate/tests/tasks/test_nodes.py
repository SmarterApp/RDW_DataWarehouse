from edmigrate.utils.constants import Constants
from edmigrate.tasks.nodes import register_slave_node,\
    get_all_registered_slave_nodes, get_registered_slave_nodes_for_group
import edmigrate.tasks.nodes
__author__ = 'sravi'

import unittest
from edcore.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite


class TestNodes(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def tearDown(self):
        global registered_slaves
        edmigrate.tasks.nodes.registered_slaves = {Constants.SLAVE_GROUP_A: [], Constants.SLAVE_GROUP_B: []}

    def test_register_slave_node(self):
        register_slave_node('testslave0.dummy.net', 'A')
        register_slave_node('testslave1.dummy.net', 'B')
        self.assertEqual(len(get_all_registered_slave_nodes()), 2)

    def test_register_slave_multiple_times(self):
        register_slave_node('testslave1.dummy.net', 'B')
        register_slave_node('testslave1.dummy.net', 'B')
        register_slave_node('testslave1.dummy.net', 'B')
        self.assertEqual(len(get_all_registered_slave_nodes()), 1)

    def test_get_registered_slave_nodes_for_group(self):
        register_slave_node('testslave1.dummy.net', 'B')
        register_slave_node('testslave2.dummy.net', 'A')
        register_slave_node('testslave3.dummy.net', 'B')
        grp_A = get_registered_slave_nodes_for_group(Constants.SLAVE_GROUP_A)
        grp_B = get_registered_slave_nodes_for_group(Constants.SLAVE_GROUP_B)
        self.assertEqual(len(grp_A), 1)
        self.assertEqual(len(grp_B), 2)

    def test_add_to_invalid_group(self):
        grp_invalid = register_slave_node('testslave1.dummy.net', 'C')
        self.assertIsNone(grp_invalid)


if __name__ == "__main__":
    unittest.main()
