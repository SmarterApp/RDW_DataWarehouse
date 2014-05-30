'''
Created on Dec 19, 2013

@author: ejen
'''
import unittest
import os
from edextract.utils.data_archiver import (import_recipient_keys, archive_files, encrypted_archive_files,
                                           GPGPublicKeyException, GPGException, archive_unencrypted_files)
import tempfile


class MockKeyserver():

    def __init__(self, keyid, key):
        self.ring = {keyid: key}

    def get_key(self, key_id):
        try:
            return self.ring[key_id]
        except Exception:
            return None

    def search_key(self, key):
        owners = self.ring.keys()
        if key in owners:
            return [{'keyid': key}]
        else:
            return []


class MockGnuPG():

    def __init__(self):
        self.ring = {}

    def search_keys(self, recipients, keyserver):
        return keyserver.search_key(recipients)

    def list_keys(self):
        return self.ring.values()

    def recv_keys(self, keyserver, recipients):
        key = keyserver.get_key(recipients)
        if key is not None:
            self.ring[recipients] = key


class Test_FileUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_recipient_keys(self):
        settings = {
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com'
        }
        gpg = MockGnuPG()
        keyserver = MockKeyserver('kswimberly@amplify.com', 'fake key')
        recipients = settings['extract.gpg.public_key.cat']
        import_recipient_keys(gpg, recipients, keyserver)
        self.assertEqual(len(gpg.list_keys()), 1)

    def test_archive_files(self):
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as dir:
            for file in files:
                with open(os.path.join(dir, file), 'a') as f:
                    f.write(file)
            data = archive_files(dir)
            fixture_len = 343
            self.assertEqual(len(data.getvalue()), fixture_len)

    def test_encrypted_archive_files_public_key_exception(self):
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        settings = {
            'extract.gpg.keyserver': 'hello',
            'extract.gpg.homedir': gpg_home,
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com'
        }
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as dir:
            for file in files:
                with open(os.path.join(dir, file), 'a') as f:
                    f.write(file)
            recipients = settings['extract.gpg.public_key.cat']
            outputfile = os.path.join(dir, 'test_ouput.gpg')
            homedir = os.path.abspath(settings['extract.gpg.homedir'])
            self.assertTrue(os.path.exists(homedir))
            keyserver = settings['extract.gpg.keyserver']
            self.assertRaises(GPGPublicKeyException, encrypted_archive_files, dir, recipients, outputfile, homedir=homedir, keyserver=keyserver, gpgbinary='gpg')

    def test_encrypted_archive_files_unrecoverable_exception(self):
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        settings = {
            'extract.gpg.keyserver': 'hello',
            'extract.gpg.homedir': gpg_home,
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com'
        }
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as dir:
            for file in files:
                with open(os.path.join(dir, file), 'a') as f:
                    f.write(file)
            recipients = settings['extract.gpg.public_key.cat']
            outputfile = os.path.join(dir, 'test_ouput.gpg')
            homedir = os.path.abspath(settings['extract.gpg.homedir'])
            self.assertTrue(os.path.exists(homedir))
            keyserver = settings['extract.gpg.keyserver']
            self.assertRaises(GPGException, encrypted_archive_files, dir, recipients, outputfile, homedir=homedir, keyserver=keyserver, gpgbinary='gpg111')

    def test_encrypted_archive_files(self):
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        settings = {
            'extract.gpg.keyserver': None,
            'extract.gpg.homedir': gpg_home,
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com'
        }
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as dir:
            for file in files:
                with open(os.path.join(dir, file), 'a') as f:
                    f.write(file)
            recipients = settings['extract.gpg.public_key.cat']
            outputfile = os.path.join(dir, 'test_ouput.gpg')
            homedir = os.path.abspath(settings['extract.gpg.homedir'])
            self.assertTrue(os.path.exists(homedir))
            keyserver = settings['extract.gpg.keyserver']
            encrypted_archive_files(dir, recipients, outputfile, homedir=homedir, keyserver=keyserver, gpgbinary='gpg')
            self.assertTrue(os.path.isfile(outputfile))
            self.assertNotEqual(os.stat(outputfile).st_size, 0)

    def test_archive_unencrypted_files(self):
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as dir:
            for file in files:
                with open(os.path.join(dir, file), 'a') as f:
                    f.write(file)
            outputfile = os.path.join(dir, 'test_output.zip')
            archive_unencrypted_files(dir, outputfile)
            self.assertTrue(os.path.isfile(outputfile))
            self.assertNotEqual(os.stat(outputfile).st_size, 0)

if __name__ == "__main__":
    unittest.main()
