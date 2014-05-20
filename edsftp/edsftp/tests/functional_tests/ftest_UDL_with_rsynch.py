'''
Created on Oct 25, 2013

@author: bpatel
'''
import unittest
import pysftp
import sys
import os
import argparse
import paramiko


class rsynch_validation(unittest.TestCase):

    def setUp(self):
        self.test_rsynch_conf = {'remote_server': 'edwappsrv5.poc.dum.edwdc.net',
                                 'file': '/Users/Shared/Amplify/edware/sftp/tests/data/test_source_file_tar_gzipped.tar.gz.gpg'}

    def testdropfile_to_remote(self):

        local_file = self.test_rsynch_conf['file']
        srv = pysftp.Connection(host=self.test_rsynch_conf['remote_server'], username="test_user",
                                password="test_user123")

        # Make no file is on remote server(app server 5)
        data = srv.listdir('/filedrop')
        self.assertEqual(0, len(data))

        # To upload the file
        srv.put(local_file, 'filedrop/' + os.path.basename(local_file))

        data = srv.listdir('/filedrop')
        print("new file")
        print(len(data))
        if len(data) != 0:
            for i in data:
                self.assertEqual(i, 'test_source_file_tar_gzipped.tar.gz.gpg')

        # Closes the connection
        srv.close()

    def testnew(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect('edwappsrv6.poc.dum.edwdc.net', username='udl2', password="udl2")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls /opt/wgen/edware-udl/zones/landing/history/test_tenant')
        print("output", ssh_stdout.read())
        ssh.close()

if __name__ == '__main__':
    unittest.main()
