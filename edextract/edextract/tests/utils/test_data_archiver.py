'''
Created on Nov 12, 2013

@author: dip
'''
import unittest
import os
import shutil
from edextract.utils.data_archiver import import_recipient_keys, remove_temp_keyring,\
    archive_files, encrypted_archive_files
import tempfile
import gnupg
from edextract.settings.config import Config, get_setting, setup_settings


class Test_FileUtils(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.mkdtemp(dir='/tmp')
        self.__mock_zip_dir = tempfile.mkdtemp(dir='/tmp')
        self.__mock_zip_dir_2 = tempfile.mkdtemp(dir='/tmp')
        dirs = [self.__mock_zip_dir, self.__mock_zip_dir_2]
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        for dir in dirs:
            for file in files:
                f = open(dir + os.sep + file, 'a')
                f.write(file)
                f.close()
        self.__mock_keyring_dir = tempfile.mkdtemp(dir='/tmp')
        self.__mock_keyring_dir_2 = tempfile.mkdtemp(dir='/tmp')
        dirs = [self.__mock_keyring_dir, self.__mock_keyring_dir_2]
        # create mock keyring files
        files = ['ks_pub.key', 'pubring.gpg', 'pubring.gpg~', 'random_seed', 'secring.gpg', 'trustdb.gpg']
        for dir in dirs:
            for file in files:
                open(dir + os.sep + file, 'a').close()

    def tearDown(self):
        dirs = [self.__temp_dir, self.__mock_zip_dir, self.__mock_keyring_dir, self.__mock_zip_dir_2, self.__mock_keyring_dir_2]
        for dir in dirs:
            shutil.rmtree(dir, ignore_errors=True)

    def test_import_recipient_keys(self):
        settings = {
            'extract.gpg.keyserver': 'hkp://edwappsrv3.poc.dum.edwdc.net',
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com'
        }
        setup_settings(settings)
        self.assertEqual(os.path.exists(self.__temp_dir), True)
        gpg = gnupg.GPG(gnupghome=os.path.abspath(self.__temp_dir), gpgbinary='gpg')
        keyserver = get_setting(Config.KEYSERVER, None)
        recipients = settings['extract.gpg.public_key.cat']
        import_recipient_keys(gpg, recipients, keyserver)
        self.assertEqual(len(gpg.list_keys()), 1)

    def test_remove_temp_keyring(self):
        self.assertEqual(os.path.exists(self.__mock_keyring_dir), True)
        remove_temp_keyring(self.__mock_keyring_dir)
        self.assertEqual(os.path.exists(self.__mock_keyring_dir), False)

    def test_archive_files(self):
        self.assertEqual(os.path.exists(self.__mock_zip_dir), True)
        data = archive_files(self.__mock_zip_dir)
        fixture_len = 343
        self.assertEqual(len(data.getvalue()), fixture_len)

    def test_encrypted_archive_files(self):
        settings = {
            'extract.gpg.keyserver': 'hkp://edwappsrv3.poc.dum.edwdc.net',
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com'
        }
        recipients = settings['extract.gpg.public_key.cat']
        self.assertEqual(os.path.exists(self.__mock_zip_dir_2), True)
        outputfile = self.__mock_zip_dir_2 + os.sep + 'test_ouput.gpg'
        self.assertEqual(os.path.exists(self.__mock_keyring_dir_2), True)
        homedir = self.__mock_keyring_dir_2
        keyserver = settings['extract.gpg.keyserver']
        fixture_len = 717
        encrypted_archive_files(self.__mock_zip_dir_2, recipients, outputfile, homedir=homedir, keyserver=keyserver, gpgbinary='gpg')
        self.assertEqual(os.path.isfile(outputfile), True)
        self.assertEqual(os.stat(outputfile).st_size, fixture_len)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
