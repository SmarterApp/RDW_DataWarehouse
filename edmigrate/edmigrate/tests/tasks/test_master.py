__author__ = 'sravi'

import unittest


class TestMasterWorker(unittest.TestCase):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def tearDown(self):
        pass

    def test_verify_master_slave_repl_status(self):
        import edmigrate.tasks.master as master
        master.verify_master_slave_repl_status('repmgr', ['dbpgdwr0.qa.dum.edwdc.net', 'dbpgdwr0s1.qa.dum.edwdc.net'])

if __name__ == "__main__":
    unittest.main()