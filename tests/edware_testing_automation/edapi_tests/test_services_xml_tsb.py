"""
Created on Aug 12, 2014

@author: nparoha
"""
import csv
import json
import os
import shutil
import subprocess
import tarfile
import time

import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.utils.preferences import preferences, TSB

TSB_RAW_DATA_PATH = preferences(TSB.xml) + '/'
TSB_ITEM_LEVEL_PATH = preferences(TSB.csv) + '/'
STAGING_PATH = preferences(TSB.staging)
XML_FILE_PATH = os.path.join(os.getcwd(), '..', 'resources')


@allure.feature('Smarter: Integration with TSB')
class TestTSBAPI(ApiHelper, SessionShareHelper, ExtractsHelper):
    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)
        ExtractsHelper.__init__(self, *args, **kwargs)
        ApiHelper.__init__(self, *args, **kwargs)
        self.dest = '/tmp/tsb_decrypt'

    def setUp(self):
        self.clean_up()

    def tearDown(self):
        self.clean_up()

    def clean_up(self):
        if os.path.exists(self.dest):
            shutil.rmtree(self.dest)
        for tenant in ['CA', 'ca']:
            for file_type in [TSB_ITEM_LEVEL_PATH, TSB_RAW_DATA_PATH, STAGING_PATH]:
                path = os.path.join(file_type, tenant)
                if os.path.exists(path):
                    shutil.rmtree(path)

    def test_post_iab_asessment(self):
        self.authenticate_with_oauth('gman')
        self.update_request_header("content-type", "application/xml")
        # Send first request
        here = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.abspath(os.path.join(os.path.join(here, '..'), 'resources', 'iabAsmt.xml'))
        xml_payload = self.get_xml_content(filepath)
        self.send_xml_post("/services/xml", xml_payload)
        self.check_response_code(202)
        self.check_files(
            os.path.join(TSB_RAW_DATA_PATH, "CA/2015/SUMMATIVE/20150727/ELA/3/2222/"),
            time.strftime('%Y%m%d'),
            "xml",
            1
        )
        batcher = '/opt/edware/test/tsbBatcher.sh'
        if os.path.exists(batcher):
            self.decrypt_untar(batcher)
            csv_file = os.path.join(self.dest, 'SBAC-FT-SomeDescription-Math-11.csv')
            self.assertTrue(os.path.exists(csv_file))
            json_file = os.path.join(self.dest, 'SBAC-FT-SomeDescription-Math-11.json')
            self.assertTrue(os.path.exists(json_file))
            with open(csv_file) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                count = 0
                for _ in reader:
                    count += 1
                self.assertEqual(count, 2)
            with open(json_file) as f:
                json_obj = json.load(f)
                self.assertEqual(json_obj['Identification']['Guid'], 'SBAC-FT-SomeDescription-Math-11')
                self.assertEqual(json_obj['Identification']['Subject'], 'Math')
                self.assertEqual(json_obj['Claims']['Claim1']['Name'], 'Algebra and Functions - Linear Functions')

    def test_post_multi_files_tsb(self):
        ## Sends a valid item level xml and validates that the Raw Data and Item Level Data is extracted.
        self.authenticate_with_oauth('gman')
        self.update_request_header("content-type", "application/xml")

        # Send first request
        here = os.path.abspath(os.path.dirname(__file__))
        filepath1 = os.path.abspath(os.path.join(os.path.join(here, '..'), 'resources', 'iabAsmt.xml'))
        xml_payload = self.get_xml_content(filepath1)
        self.send_xml_post("/services/xml", xml_payload)
        self.check_response_code(202)
        # Send second request
        here = os.path.abspath(os.path.dirname(__file__))
        filepath2 = os.path.abspath(os.path.join(os.path.join(here, '..'), 'resources', 'valid_tsb1.xml'))
        xml_payload = self.get_xml_content(filepath2)
        self.send_xml_post("/services/xml", xml_payload)
        self.check_response_code(202)
        self.check_files(
            os.path.join(TSB_RAW_DATA_PATH, "CA/2015/SUMMATIVE/20150727/ELA/3/2222/"),
            time.strftime('%Y%m%d'),
            "xml",
            2
        )

        # This is for jenkins test
        batcher = '/opt/edware/test/tsbBatcher.sh'
        if os.path.exists(batcher):
            self.decrypt_untar(batcher)
            csv_file = os.path.join(self.dest, 'SBAC-FT-SomeDescription-ELA-7.csv')
            self.assertTrue(os.path.exists(csv_file))
            json_file = os.path.join(self.dest, 'SBAC-FT-SomeDescription-ELA-7.json')
            self.assertTrue(os.path.exists(json_file))
            with open(csv_file) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                count = 0
                for _ in reader:
                    count += 1
                self.assertEqual(count, 3)
            with open(json_file) as f:
                json_obj = json.load(f)
                self.assertEqual(json_obj['Identification']['Guid'], 'SBAC-FT-SomeDescription-ELA-7')
                self.assertEqual(json_obj['Identification']['Subject'], 'ELA')

    def test_valid_content_type_no_payload(self):
        ## Sends a request with a valid content type but No XML payload
        self.authenticate_with_oauth('gman')
        self.update_request_header("content-type", "application/xml")
        self.send_xml_post("/services/xml", "")
        self.check_response_code(412)

    def test_valid_content_type_invalid_xml_payload(self):
        ## Sends a request with a valid content type but No XML payload
        self.authenticate_with_oauth('gman')
        self.update_request_header("content-type", "application/xml")
        here = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.abspath(os.path.join(os.path.join(here, '..'), 'resources', 'invalid_tsb.xml'))
        xml_payload = self.get_xml_content(filepath)
        self.send_xml_post("/services/xml", xml_payload)
        self.check_response_code(412)

    def decrypt_untar(self, batcher):
        subprocess.Popen(['sh', batcher])
        staging_path = os.path.join(STAGING_PATH, 'ca')
        self.assertTrue(os.path.exists(staging_path))
        batch = None
        for f in os.listdir(staging_path):
            file_path = os.path.join(staging_path, f)
            if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.gpg':
                batch = file_path
        self.decrypt_gpg_file(os.path.basename(batch), os.path.dirname(batch), self.dest, '/var/lib/jenkins/.gnupg',
                              '/usr/bin/gpg', decrypted_file='extract.tar.gz', passphrase='sbac udl2')
        target = os.path.join(self.dest, 'extract.tar.gz')
        self.assertTrue(os.path.exists(target))
        tar = tarfile.open(target)
        tar.extractall(path=self.dest)
        tar.close()

    def check_files(self, filepath, fileprefix, fileextn, count_of_files):
        assert (os.path.isdir(filepath))
        all_files = []
        for file in os.listdir(filepath):
            if not file.startswith('.'):
                all_files.append(file)
                if not (fileprefix in file and file.endswith(fileextn)):
                    raise Exception('Incorrect file found: {f}'.format(f=file))
        self.assertEqual(len(all_files), count_of_files)

    def get_xml_content(self, filepath):
        """
        returns the XML content from the XML file
        :param filepath: XML file path
        :type filepath: string
        :return f.read(): XML data to post in the payload
        :type f.read(): string
        """
        f = open(filepath)
        return f.read()

    def check_metadata(self, filepath, expected_lines):
        print("here")
        print(filepath)
        num_lines = len(expected_lines)
        print(num_lines)
        actual_lines = []
        count = 0
        with open(filepath) as fp:
            for line in fp:
                actual_lines.append(str(line))
                count += 1
        self.assertEqual(num_lines, count, "%s number of lines not found in .metadata file." % num_lines)
        for filename in expected_lines:
            found = False
            if found is False:
                for each_line in actual_lines:
                    if filename in each_line:
                        found = True
                        break
            self.assertTrue(found, "%s not found in .metadata" % filename)
