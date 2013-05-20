'''
Created on May 17, 2013

@author: tosako
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from edapi.exceptions import NotFoundException
import os
from smarter.reports.helpers.ISR_pdf_name_formatter import ISR_pdf_name


class Test(Unittest_with_smarter_sqlite):

    def test_ISR_pdf_filename(self):
        pdf_filename_formatter = ISR_pdf_name(studentGuid='61ec47de-e8b5-4e78-9beb-677c44dd9b50')
        file_name = pdf_filename_formatter.generate_filename()
        self.assertEqual(file_name, "61ec47de-e8b5-4e78-9beb-677c44dd9b50")

    def test_ISR_pdf_filename_studentguid_not_exist(self):
        with self.assertRaises(NotFoundException):
            pdf_filename_formatter = ISR_pdf_name(studentGuid='ff1c2b1a-c15d-11e2-ae11-3c07546832b4')
            pdf_filename_formatter.generate_filename()

    def test_ISR_pdf_directory_name(self):
        pdf_filename_formatter = ISR_pdf_name(studentGuid='61ec47de-e8b5-4e78-9beb-677c44dd9b50')
        dir_name = pdf_filename_formatter.generate_dirname()
        self.assertEqual(dir_name, os.path.join('NY', '2012', '228', '242', '3', 'SUMMATIVE'))

    def test_ISR_pdf_directory_name_studentguid_not_exist(self):
        with self.assertRaises(NotFoundException):
            pdf_filename_formatter = ISR_pdf_name(studentGuid='ff1c2b1a-c15d-11e2-ae11-3c07546832b4')
            pdf_filename_formatter.generate_dirname()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
