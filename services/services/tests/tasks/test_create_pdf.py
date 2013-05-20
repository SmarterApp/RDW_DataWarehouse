'''
Created on May 14, 2013

@author: dip
'''
import unittest
import services
from services.tasks.create_pdf import generate_pdf, OK, FAIL, get_pdf_file
import platform
import os


class TestCreatePdf(unittest.TestCase):

    def test_generate_pdf_success_cmd(self):
        services.tasks.create_pdf.pdf_procs = ['echo', 'dummy']
        task = generate_pdf('cookie', 'url', 'outputfile')
        self.assertEqual(task, OK)

    def test_generate_pdf_timeout_with_output_file_generated(self):
        here = os.path.abspath(__file__)
        services.tasks.create_pdf.pdf_procs = self.__get_cmd()
        task = generate_pdf('cookie', 'url', here, options=[], timeout=1)
        self.assertEqual(task, OK)

    def test_generate_pdf_timeout_without_output_file_generated(self):
        cur_dir = os.path.dirname(__file__)
        output_file = os.path.abspath(os.path.join(cur_dir, 'doesnotexist.out'))
        services.tasks.create_pdf.pdf_procs = self.__get_cmd()
        task = generate_pdf('cookie', 'url', output_file, options=[], timeout=1)
        self.assertEqual(task, FAIL)

    def test_generate_pdf_fail_cmd(self):
        services.tasks.create_pdf.pdf_procs = ['dummycmd']
        task = generate_pdf('cookie', 'url', 'outputfile')
        self.assertEqual(task, FAIL)

    def test_get_pdf_invalid_file(self):
        file_name = '/tmp/i_dont_exist'
        task = get_pdf_file(file_name)
        self.assertIsNone(task)

    def test_get_pdf_valid_file(self):
        here = os.path.abspath(__file__)
        task = get_pdf_file(here)
        self.assertIsNotNone(task)

    def __get_cmd(self):
        '''
        Based on os type, return the command to execute test script
        '''
        cur_dir = os.path.dirname(__file__)
        test_file = os.path.abspath(os.path.join(cur_dir, '..', 'resources', 'sleep.sh'))
        cmd = ['sh', test_file]
        if platform.system() == 'Windows':
            test_file = os.path.abspath(os.path.join(cur_dir, '..', 'resources', 'sleep.cmd'))
            cmd = [test_file]
        return cmd


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
