'''
Created on May 14, 2013

@author: dip
'''
import unittest
import services
from services.tasks.pdf import generate, OK, \
    prepare_path, get, is_valid, delete
from services.celeryconfig import setup_global_settings
import platform
import os
import tempfile
import shutil
from services.exceptions import PdfGenerationError


class TestCreatePdf(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.mkdtemp()
        settings = {'pdf.minimum.file.size': '1'}
        setup_global_settings(settings)

    def tearDown(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)

    def test_generate_pdf_success_cmd(self):
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        file_name = os.path.join(self.__temp_dir, 'b', 'd.pdf')
        prepare_path(file_name)
        with open(file_name, 'w') as file:
            file.write('%PDF-1.4')
        task = generate('cookie', 'url', file_name)
        self.assertEqual(task, OK)

    def test_generate_pdf_timeout_with_output_file_generated(self):
        here = os.path.abspath(__file__)
        services.tasks.pdf.pdf_procs = get_cmd()
        task = generate('cookie', 'url', here, options=[], timeout=1)
        self.assertEqual(task, OK)

    def test_generate_pdf_timeout_without_output_file_generated(self):
        cur_dir = os.path.dirname(__file__)
        output_file = os.path.abspath(os.path.join(cur_dir, 'doesnotexist.out'))
        services.tasks.pdf.pdf_procs = get_cmd()
        self.assertRaises(PdfGenerationError, generate, 'cookie', 'url', output_file, options=[], timeout=1)

    def test_generate_with_retries(self):
        settings = {'pdf.minimum.file.size': '1000000'}
        setup_global_settings(settings)
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        file_name = os.path.join(self.__temp_dir, 'b', 'd.pdf')
        self.assertRaises(PdfGenerationError, generate, 'cookie', 'url', file_name, timeout=1)

    def test_generate_pdf_fail_cmd(self):
        services.tasks.pdf.pdf_procs = ['dummycmd']
        self.assertRaises(PdfGenerationError, generate, 'cookie', 'url', 'outputfile')

    def test_get_pdf_valid_file(self):
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        here = os.path.abspath(__file__)
        task = get('cookie', 'url', here)
        self.assertIsNotNone(task)

    def test_create_directory(self):
        file_name = os.path.join(self.__temp_dir, 'a', 'b', 'c', 'd.pdf')
        # make sure directory does not exist first.
        shutil.rmtree(os.path.dirname(file_name), ignore_errors=True)
        prepare_path(file_name)
        self.assertTrue(os.access(os.path.dirname(file_name), os.R_OK))

    def test_no_exception_when_dir_exist(self):
        file_name = os.path.join(self.__temp_dir, 'a', 'b', 'c', 'd.pdf')
        prepare_path(file_name)
        prepare_path(file_name)
        self.assertTrue(os.path.exists(os.path.dirname(file_name)))

    def test_validate_file_non_existing_file(self):
        path = os.path.join(self.__temp_dir, 'notexist.pdf')
        valid = is_valid(path)
        self.assertFalse(valid)

    def test_validate_file_existing_file(self):
        here = os.path.abspath(__file__)
        valid = is_valid(here)
        self.assertTrue(valid)

    def test_validate_file_size_too_small(self):
        settings = {'pdf.minimum.file.size': '1000000'}
        setup_global_settings(settings)
        here = os.path.abspath(__file__)
        valid = is_valid(here)
        self.assertFalse(valid)

    def test_delete_file(self):
        file_name = os.path.join(self.__temp_dir, 'i_exist')
        prepare_path(file_name)
        with open(file_name, 'w') as file:
            file.write('%PDF-1.4')
        delete(file_name)
        self.assertFalse(os.path.exists(file_name))


def get_cmd():
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
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
