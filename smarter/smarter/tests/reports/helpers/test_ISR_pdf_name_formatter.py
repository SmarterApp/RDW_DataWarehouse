'''
Created on May 17, 2013

@author: tosako
'''
import unittest
import os

from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from pyramid.security import Allow

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edapi.exceptions import NotFoundException
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid, \
    generate_isr_absolute_file_path_name
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map
from smarter.security.roles.pii import PII  # @UnusedImport


class TestISRPdfNameFormatter(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['cache.expire'] = 10
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def test_generate_isr_report_path_by_student_guid(self):
        file_name = generate_isr_report_path_by_student_guid('NC', '20160404', pdf_report_base_dir='/', student_guid='61ec47de-e8b5-4e78-9beb-677c44dd9b50')
        self.assertEqual(file_name, os.path.join('/', 'NC', '2016', '228', '242', '4', 'isr', 'SUMMATIVE', '61ec47de-e8b5-4e78-9beb-677c44dd9b50.20160404.en.pdf'))

    def test_generate_isr_report_path_by_student_guid_studentguid_not_exist(self):
        self.assertRaises(NotFoundException, generate_isr_report_path_by_student_guid, 'NC', '20120101', pdf_report_base_dir='/', student_guid='ff1c2b1a-c15d-11e2-ae11-3c07546832b4')

    def test_generate_isr_absolute_file_path_name(self):
        file_name = generate_isr_absolute_file_path_name(pdf_report_base_dir='/', state_code='FL', asmt_period_year='2013', district_guid='123', school_guid='456', asmt_grade='1', student_guid='1bc-def-ad', asmt_type='SUMMATIVE', effective_date='20120201')
        self.assertEqual(file_name, os.path.join('/', 'FL', '2013', '123', '456', '1', 'isr', 'SUMMATIVE', '1bc-def-ad.20120201.en.pdf'))

    def test_generate_isr_report_path_by_student_guid_for_grayScale(self):
        file_name = generate_isr_report_path_by_student_guid('NC', '20160404', pdf_report_base_dir='/', student_guid='61ec47de-e8b5-4e78-9beb-677c44dd9b50', grayScale=True, lang='jp')
        self.assertEqual(file_name, os.path.join('/', 'NC', '2016', '228', '242', '4', 'isr', 'SUMMATIVE', '61ec47de-e8b5-4e78-9beb-677c44dd9b50.20160404.jp.g.pdf'))

    def test_generate_isr_report_path_by_student_guid_studentguid_not_existd_for_grayScale(self):
        self.assertRaises(NotFoundException, generate_isr_report_path_by_student_guid, 'NC', '20120201', pdf_report_base_dir='/', student_guid='ff1c2b1a-c15d-11e2-ae11-3c07546832b4', grayScale=True)

    def test_generate_isr_absolute_file_path_named_for_grayScale(self):
        file_name = generate_isr_absolute_file_path_name(pdf_report_base_dir='/', state_code='FL', asmt_period_year='2013', district_guid='123', school_guid='456', asmt_grade='1', student_guid='1bc-def-ad', asmt_type='SUMMATIVE', grayScale=True, effective_date='20120201')
        self.assertEqual(file_name, os.path.join('/', 'FL', '2013', '123', '456', '1', 'isr', 'SUMMATIVE', '1bc-def-ad.20120201.en.g.pdf'))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
