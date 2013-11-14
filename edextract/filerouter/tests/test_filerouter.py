'''
Created on Nov 14, 2013

@author: tosako
'''
import unittest
import tempfile
import os
import shutil
from filerouter import filerouter


class Test(unittest.TestCase):

    SFTP_BASE = 'sftp'
    JAIL_HOME_BASE = os.path.join('opt', 'edware', 'home')
    JAIL_GATEKEEPER_ACCOUNT_BASE = 'departures'
    FILE_ROUTER_ACCOUNTE = 'file_router'
    GATEKEEPER_TEST_USERNAME1 = os.path.join('ca', 'kswimberly')
    GATEKEEPER_TEST_USERNAME2 = os.path.join('ny', 'byip')
    GATEKEEPER_TEST_USERNAME3 = os.path.join('hi', 'hacker')

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(suffix='.test_filerouter')
        self.file_router_home_dir = os.path.join(self.temp_dir, self.SFTP_BASE, self.JAIL_HOME_BASE, self.FILE_ROUTER_ACCOUNTE)
        extra_file = False
        for gatekeeper in [self.GATEKEEPER_TEST_USERNAME1, self.GATEKEEPER_TEST_USERNAME2, self.GATEKEEPER_TEST_USERNAME3]:
            route_path = os.path.join(self.file_router_home_dir, 'route', gatekeeper)
            os.makedirs(route_path, mode=0o700, exist_ok=True)
            # create empty files for test
            open(os.path.join(route_path, 'testfile1.zip'), 'a').close()
            open(os.path.join(route_path, 'testfile2.zip.partial'), 'a').close()
            if not extra_file:
                open(os.path.join(route_path, 'testfile2.zip'), 'a').close()
                extra_file = True
        self.jail_gatekeeper_account_home = os.path.join(self.temp_dir, self.SFTP_BASE, self.JAIL_HOME_BASE, self.JAIL_GATEKEEPER_ACCOUNT_BASE)
        gatekeeper1_home_dir = os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME1)
        gatekeeper2_home_dir = os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME2)
        os.makedirs(gatekeeper1_home_dir, mode=0o700, exist_ok=True)
        open(os.path.join(gatekeeper1_home_dir, 'testfile2.zip'), 'a').close()
        os.makedirs(gatekeeper2_home_dir, mode=0o700, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_find_files(self):
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, 'route'))
        self.assertEqual(4, len(files))
        route_dir = os.path.join(self.file_router_home_dir, 'route')
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, 'testfile1.zip'), files)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, 'testfile2.zip'), files)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME2, 'testfile1.zip'), files)
        self.assertIn(os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME3, 'testfile1.zip'), files)

    def test_get_destination_filename_for_gatekeeper(self):
        route_dir = os.path.join(self.file_router_home_dir, 'route')
        test_file1 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, 'testfile1.zip')
        test_file2 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME1, 'testfile2.zip')
        test_file3 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME2, 'testfile1.zip')
        test_file4 = os.path.join(route_dir, self.GATEKEEPER_TEST_USERNAME3, 'testfile1.zip')
        
        dest_file1 = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, test_file1)
        self.assertEqual(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME1, 'testfile1.zip'), dest_file1)
        dest_file2 = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, test_file2)
        self.assertEqual(os.path.join(self.file_router_home_dir, 'error', self.GATEKEEPER_TEST_USERNAME1, 'testfile2.zip'), dest_file2)
        dest_file3 = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, test_file3)
        self.assertEqual(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME2, 'testfile1.zip'), dest_file3)
        dest_file4 = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, test_file4)
        self.assertEqual(os.path.join(self.file_router_home_dir, 'error', self.GATEKEEPER_TEST_USERNAME3, 'testfile1.zip'), dest_file4)

    def test_route_file(self):
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, 'route'))
        for file in files:
            dest_file = filerouter._get_destination_filename_for_gatekeeper(self.jail_gatekeeper_account_home, file)
            filerouter._route_file(file, dest_file)
        self.assertTrue(os.path.isfile(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME1, 'testfile1.zip')))
        self.assertTrue(os.path.isfile(os.path.join(self.file_router_home_dir, 'error', self.GATEKEEPER_TEST_USERNAME1, 'testfile2.zip')))
        self.assertTrue(os.path.isfile(os.path.join(self.jail_gatekeeper_account_home, self.GATEKEEPER_TEST_USERNAME2, 'testfile1.zip')))
        self.assertTrue(os.path.isfile(os.path.join(self.file_router_home_dir, 'error', self.GATEKEEPER_TEST_USERNAME3, 'testfile1.zip')))
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, 'route'))
        self.assertEqual(0, len(files))
        files = filerouter._find_files(os.path.join(self.file_router_home_dir, 'route'), suffix='.process')
        self.assertEqual(0, len(files))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
