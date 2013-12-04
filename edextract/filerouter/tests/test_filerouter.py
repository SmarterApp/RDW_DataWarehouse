'''
Created on Nov 14, 2013

@author: tosako
'''
import unittest
import tempfile
import os
import shutil
from filerouter import filerouter
from filerouter.filerouter import GatekeeperException, FileInfo


class Test(unittest.TestCase):

    SFTP_BASE = 'sftp'
    HOME_BASE = os.path.join('opt', 'edware', 'home')
    GATEKEEPER_ACCOUNT_BASE = 'departures'
    FILE_ROUTER_ACCOUNT_NAME = 'file_router'
    GATEKEEPER_TEST_USERNAME1 = os.path.join('ca', 'kswimberly')
    GATEKEEPER_TEST_USERNAME2 = os.path.join('ny', 'byip')
    GATEKEEPER_TEST_USERNAME3 = os.path.join('hi', 'hacker')
    TESTFILE1 = 'testfile1.zip.gpg'
    TESTFILE2 = 'testfile2.zip.gpg'
    TESTFILE3 = 'testfile3.zip.gpg'
    REPORTS = 'reports'
    ROUTE = 'route'
    ERROR = 'error'
    ARCHIVE = 'archive'

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(suffix='.test_filerouter')
        self.file_router_home_dir = os.path.join(self.temp_dir, self.SFTP_BASE, self.HOME_BASE, self.FILE_ROUTER_ACCOUNT_NAME)
        self.jailed_home_base = os.path.join(self.temp_dir, self.SFTP_BASE, self.HOME_BASE, self.GATEKEEPER_ACCOUNT_BASE)
        extra_file = False
        for gatekeeper in [self.GATEKEEPER_TEST_USERNAME1, self.GATEKEEPER_TEST_USERNAME2, self.GATEKEEPER_TEST_USERNAME3]:
            route_path = os.path.join(self.file_router_home_dir, self.ROUTE, gatekeeper)
            os.makedirs(route_path, mode=0o700, exist_ok=True)
            # create empty files for test
            open(os.path.join(route_path, self.TESTFILE1), 'a').close()
            open(os.path.join(route_path, self.TESTFILE3 + '.partial'), 'a').close()
            if not extra_file:
                open(os.path.join(route_path, self.TESTFILE2), 'a').close()
                extra_file = True
        self.jail_gatekeeper_account_home = os.path.join(self.temp_dir, self.SFTP_BASE, self.HOME_BASE, self.GATEKEEPER_ACCOUNT_BASE)
        self.gatekeeper_home_base = os.path.join(self.temp_dir, self.HOME_BASE, self.GATEKEEPER_ACCOUNT_BASE)
        jail_gatekeeper1_home_dir = os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME1)
        jail_gatekeeper2_home_dir = os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME2)
        jail_gatekeeper1_home_reports_dir = os.path.join(jail_gatekeeper1_home_dir, self.REPORTS)
        os.makedirs(jail_gatekeeper1_home_reports_dir, mode=0o700, exist_ok=True)
        open(os.path.join(jail_gatekeeper1_home_reports_dir, self.TESTFILE2), 'a').close()
        os.makedirs(jail_gatekeeper2_home_dir, mode=0o700, exist_ok=True)
        gatekeeper1_home_dir = os.path.join(self.gatekeeper_home_base, self.GATEKEEPER_TEST_USERNAME1)
        gatekeeper2_home_dir = os.path.join(self.gatekeeper_home_base, self.GATEKEEPER_TEST_USERNAME2)
        os.makedirs(gatekeeper1_home_dir, mode=0o700, exist_ok=True)
        os.makedirs(gatekeeper2_home_dir, mode=0o700, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_find_files(self):
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, self.ROUTE))
        self.assertEqual(4, len(files))
        route_dir = os.path.join(self.file_router_home_dir, self.ROUTE)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, self.TESTFILE1), files)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, self.TESTFILE2), files)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME2, self.TESTFILE1), files)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME3, self.TESTFILE1), files)

    def test_get_destination_filename_for_gatekeeper(self):
        route_dir = os.path.join(self.file_router_home_dir, self.ROUTE)
        test_file1 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, self.TESTFILE1)
        test_file2 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, self.TESTFILE2)
        test_file3 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME2, self.TESTFILE1)
        test_file4 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME3, self.TESTFILE1)

        file_info = FileInfo(test_file1)
        dest_file1 = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, self.REPORTS, file_info)
        self.assertEqual(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME1, self.REPORTS, self.TESTFILE1), dest_file1)
        file_info = FileInfo(test_file2)
        self.assertRaises(GatekeeperException, filerouter._get_destination_filename_for_gatekeeper, self.jail_gatekeeper_account_home, self.REPORTS, file_info)
        file_info = FileInfo(test_file3)
        dest_file3 = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, self.REPORTS, file_info)
        self.assertEqual(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME2, self.REPORTS, self.TESTFILE1), dest_file3)
        file_info = FileInfo(test_file4)
        self.assertRaises(GatekeeperException, filerouter._get_destination_filename_for_gatekeeper, self.jail_gatekeeper_account_home, self.REPORTS, file_info)

    def test_file_routing(self):
        filerouter.file_routing(self.jailed_home_base, self.gatekeeper_home_base, self.file_router_home_dir, self.REPORTS, self.ROUTE, self.ERROR, self.ARCHIVE, False)
        self.assertTrue(os.path.isfile(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME1, self.REPORTS, self.TESTFILE1)))
        self.assertTrue(os.path.isfile(os.path.join(self.file_router_home_dir, self.ERROR, self.GATEKEEPER_TEST_USERNAME1, self.TESTFILE2)))
        self.assertTrue(os.path.isfile(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME2, self.REPORTS, self.TESTFILE1)))
        self.assertTrue(os.path.isfile(os.path.join(self.file_router_home_dir, self.ERROR, self.GATEKEEPER_TEST_USERNAME3, self.TESTFILE1)))
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, self.ROUTE))
        self.assertEqual(0, len(files))
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, self.ROUTE), suffix='.process')
        self.assertEqual(0, len(files))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
