'''
Created on Oct 25, 2013

@author: bpatel
'''
import unittest
import pysftp
import sys
import os
import argparse


class rsynch_validation(unittest.TestCase):

    def setUp(self):
        self.test_rsynch_conf = {
                                 'remote_server': 'edwappsrv5.poc.dum.edwdc.net',
                                 'file': '/Users/Shared/Amplify/edware/sftp/tests/data/test_source_file_tar_gzipped.tar.gz.gpg'
                                 }

    def testdropfile_to_remote(self):

        local_file = self.test_rsynch_conf['file']
        srv = pysftp.Connection(host=self.test_rsynch_conf['remote_server'], username="test_user",
                            password="test_user123")

        # Make no file is on remote server(app server 5)
        data = srv.listdir('/filedrop')
        self.assertEqual(0, len(data))

        # To upload the file
        srv.put(local_file, 'filedrop/' + os.path.basename(local_file))

        #Assert file is loded to remote server (appserver5)

        data = srv.listdir('/filedrop')
        print("new file")
        print(len(data))
        if (len(data) != 0):
            for i in data:
                self.assertEqual(i, 'test_source_file_tar_gzipped.tar.gz.gpg')

        # Closes the connection
        srv.close()
if __name__ == '__main__':
    unittest.main()
