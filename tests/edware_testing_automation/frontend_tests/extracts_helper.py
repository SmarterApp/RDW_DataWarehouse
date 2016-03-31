# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'smuhit'

import csv
import fnmatch
import os
import re
import time
import zipfile

import gnupg

from edware_testing_automation.utils.test_base import EdTestBase


class ExtractsHelper(EdTestBase):
    def __init__(self, *args, **kwargs):
        EdTestBase.__init__(self, *args, **kwargs)

    def remove_extract_directory(self, sftp_dir, encrypted_dir, decrypted_dir, unzipped_dir, tenant='cat'):
        """
        Changes file permission and deletes the following directories
        Extract working directory - /tmp/{tenant}
        Jail account directory - sftp_dir
        Deletes the test directory used for copying the zip file, unzipping & decrypting it
        """
        os.system("sudo /bin/chmod -R a+r " + sftp_dir)
        os.system("sudo /bin/chmod -R a+r /tmp/{0}".format(tenant))
        os.system("sudo /bin/rm -rf " + sftp_dir)
        print("Deleted SFTP_DIR_PATH")
        os.system("sudo /bin/rm -rf /tmp/{0}".format(tenant))
        print("Deleted /tmp/{0}".format(tenant))
        os.system("rm -rf " + unzipped_dir)
        os.system("rm -rf " + decrypted_dir)
        os.system("rm -rf " + encrypted_dir)

    def get_csv_download_filename_and_url(self, success_message, report_type):
        """
        Gets the zipfile name from the success message
        :param success_message: Success message received after sending the request.
        :param success_message: string
        """
        text1 = "Your request for {0} made on".format(report_type)
        text2 = "24 hours to download the requested report. The name of your file is "
        self.assertIn(text1, success_message, "Success message incorrectly displayed.")
        self.assertIn(text2, success_message, "Success message incorrectly displayed.")
        # Strip off the filename from the success message
        filename = re.search('The name of your file is ([^\s]+)', success_message).group(1)[:-1]
        # Strip off the url from the success message
        url = re.search('You can retrieve your file from the following link ([^\s]+)', success_message)
        if url:
            url = url.group(1)
        print("Successfully validated the success message after an extract request was sent.")
        print(filename)
        return filename, url

    def run_file_routing_program(self, sftp_dir, tenant='cat'):
        """
        Checks the zip file existence in the working directory.
        Once the zip file is found in the working directory, jenkins_filerouter.sh is executed.
        Checks that reports directory is created in the jail account directory
        """
        # Check for zip file existence in the working directory
        working_dir_found = False
        jailaccount_dir_found = False
        timeout_working_dir = 0
        timeout_jailbreak_dir = 0
        while working_dir_found is False and timeout_working_dir <= 20:
            time.sleep(5)
            try:
                os.system("sudo /bin/chmod -R a+r /tmp/{0}".format(tenant))
                working_dir_found = os.system("sudo /tmp/{0}".format(tenant))
            except:
                timeout_working_dir += 5
        self.assertTrue(working_dir_found, "Did not find the zip.gpg file in the Extract working directory")

        # Run the File Routing Program and check for Reports directory in the Jail Account directory
        os.system("sudo /usr/local/bin/jenkins_filerouter.sh")
        while jailaccount_dir_found is False and timeout_jailbreak_dir <= 20:
            time.sleep(2)
            try:
                os.system("sudo /bin/chmod -R a+r {0}".format(sftp_dir))
                jailaccount_dir_found = os.system("sudo  " + sftp_dir)
            except:
                timeout_jailbreak_dir += 5
        self.assertTrue(jailaccount_dir_found,
                        "Did not find the zip file in the Extract jail account directory " + sftp_dir)
        print("Successfully sent a request to run the file routing program")

    def check_file_directory(self, filename, sftp_dir):
        """
        Check that the zip file is available inside the jail account directory
        :param filename: Zip file name
        :type filename: string
        :param sftp_dir: STFP directory path
        """
        file_path = sftp_dir + "/" + filename
        assert os.system("sudo  " + file_path)

    def find_file(self, filename, tenant):
        time.sleep(10)
        for root, dirs, files in os.walk("/tmp/{0}".format(tenant)):
            if filename in files:
                return os.path.join(root, filename)

    def copy_gpg_file_FT_dir(self, filename, sftp_dir, encrypted_dir):
        """
        Creates the encrypted_files directory and copies the gpg file from the jail account directory to this one.
        :param filename: GPG file name
        :type filename: string
        """
        if not os.path.exists(encrypted_dir):
            os.makedirs(encrypted_dir)
        print("Made encrypted_files directory")
        # Copy the .zip.gpg file from the /sftp/.../reports/ dir to the /tmp/FTs_extracted_files/encrypted_files dir
        if sftp_dir:
            file_path = sftp_dir + "/" + filename
        else:
            file_path = filename
        os.system("sudo /bin/chmod -R a+r " + file_path)
        os.system("sudo cp " + file_path + " " + encrypted_dir)

    def decrypt_gpg_file(self, gpg_filename, encrypted_dir, decrypted_dir, gnupg_home_path, gpg_binary_path,
                         decrypted_file='extract.zip', passphrase='edware1234'):
        """
        Creates the decrypted_dir directory and decrypts the GPG file from the 'encrypted_files' directory in extract.zip file
        :param gpg_filename: GPG file name
        :type gpg_filename: string
        """
        if not os.path.exists(decrypted_dir):
            os.makedirs(decrypted_dir)
        gpg_file_path = os.path.join(encrypted_dir, gpg_filename)
        # Assumption: Unzipped file *.csv.gpg is available to be decrypted
        gpg = gnupg.GPG(gnupghome=gnupg_home_path, gpgbinary=gpg_binary_path)
        DECRYPTED_FILE_PATH = os.path.join(decrypted_dir, decrypted_file)
        # Open the *.csv.gpg file and start decrypting the contents in a csv file mentioned above
        with open(gpg_file_path) as f:
            status = gpg.decrypt_file(f, passphrase=passphrase, output=DECRYPTED_FILE_PATH)
        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)

    def unzip_file(self, decrypted_dir, unzipped_dir):
        """
        Unzips the extract.zip file inside decrypted_dir directory to the unzipped_dir directory
        """
        unzip_found = False
        # unzip the file
        zip_file_path = decrypted_dir + "extract.zip"
        os.system("sudo /bin/chmod -R a+r " + zip_file_path)
        print(zip_file_path)
        with zipfile.ZipFile(zip_file_path) as unzipped_file:
            unzipped_file.extractall(unzipped_dir)
        print("Unzipped the file inside decrypted_files directory.")

    def unzip_file_to_directory(self, file_to_unzip, unzipped_dir):
        while os.path.getsize(file_to_unzip) == 0:
            time.sleep(0.1)
        with zipfile.ZipFile(file_to_unzip) as unzipped_file:
            unzipped_file.extractall(unzipped_dir)

    def get_file_names(self, unzipped_dir):
        """
        Gets the.csv and json file names from the unzipped_files
        :return [csv_file_names, json_file_names]: list of csv file names list and json file names list
        :type [csv_file_names, json_file_names]: list
        """
        csv_file_names = []
        json_file_names = []
        for file in os.listdir(unzipped_dir):
            if fnmatch.fnmatch(file, '*.csv'):
                csv_file_names.append(str(file))
            # print file
            elif fnmatch.fnmatch(file, '*.json'):
                json_file_names.append(str(file))
        return [csv_file_names, json_file_names]

    def validate_expected_headers(self, file_path, expected_headers):
        with open(file_path) as f:
            reader = csv.reader(f)
            actual_headers = next(reader)
            self.assertEqual(len(actual_headers), len(expected_headers), "Column Count is incorrect in the csv report")
            self.assertEqual(actual_headers, expected_headers)
        f.close()

    def validate_item_level_csv_headers(self, file_path):
        expected_headers = ['key', 'studentId', 'segmentId', 'position', 'clientId',
                            'operational', 'isSelected', 'format', 'score', 'scoreStatus', 'adminDate',
                            'numberVisits', 'strand', 'contentLevel', 'pageNumber', 'pageVisits', 'pageTime', 'dropped']
        self.validate_expected_headers(file_path, expected_headers)

    def validate_sr_completion_report_csv_headers(self, year, file_path):
        expected_headers = ['State', 'District', 'School', 'Category', 'Value',
                            'AY{0} Count of Registered Students'.format(year),
                            'AY{0} Count of Students Assessed by Summative Math'.format(year),
                            'AY{0} Percent of Registered Students Assessed by Summative Math'.format(year),
                            'AY{0} Count of Students Assessed by Summative ELA'.format(year),
                            'AY{0} Percent of Registered Students Assessed by Summative ELA'.format(year),
                            'AY{0} Count of Students Assessed by Interim Comprehensive Math'.format(year),
                            'AY{0} Percent of Registered Students Assessed by Interim Comprehensive Math'.format(year),
                            'AY{0} Count of Students Assessed by Interim Comprehensive ELA'.format(year),
                            'AY{0} Percent of Registered Students Assessed by Interim Comprehensive ELA'.format(year)]
        self.validate_expected_headers(file_path, expected_headers)

    def validate_sr_statistics_report_csv_headers(self, year, file_path):
        expected_headers = ['State', 'District', 'School', 'Category', 'Value', 'AY{0} Count'.format(year - 1),
                            'AY{0} Percent of Total'.format(year - 1), 'AY{0} Count'.format(year),
                            'AY{0} Percent of Total'.format(year), 'Change in Count', 'Percent Difference in Count',
                            'Change in Percent of Total', 'AY{0} Matched IDs to AY{1} Count'.format(year, year - 1),
                            'AY{0} Matched IDs Percent of AY{1} Count'.format(year, year - 1)]
        self.validate_expected_headers(file_path, expected_headers)

    def validate_csv_files_match(self, expected_file, actual_file):
        expected_csv = list(csv.reader(open(expected_file)))
        actual_csv = list(csv.reader(open(actual_file)))
        self.assertEqual(expected_csv, actual_csv)
