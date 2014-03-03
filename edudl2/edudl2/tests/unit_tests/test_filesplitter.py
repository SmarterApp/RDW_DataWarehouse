import unittest
import os
import shutil
import csv
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.filesplitter.file_splitter import create_output_destination,\
    run_command, get_list_split_files
import tempfile


class Test(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        udl2_conf = conf_tup[0]
        self.conf = udl2_conf
        #define test file name and directory
        self.test_output_path = udl2_conf['zones']['tests'] + 'this/is/a/'
        self.test_file_name = 'test.csv'
        self.output_dir = tempfile.mkdtemp()
        self.output_template = 'split_part_'
        return

    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_create_output_dest(self):
        #if directory exists, delete it
        base = os.path.splitext(os.path.basename(self.test_file_name))[0]
        root = '/'.join(self.test_output_path.split('/')[0:-3]) + '/'
        output_dir = os.path.join(self.test_output_path, base)
        if os.path.exists(output_dir):
            shutil.rmtree(root)
        #call function to create output destination
        template, directory = create_output_destination(self.test_file_name, self.test_output_path + '/' + base)
        #check if directory created correctly
        self.assertTrue(os.path.exists(output_dir))
        self.assertEqual(template, 'test_part_')
        #clean up test directory
        #shutil.rmtree(root)

    def test_run_command(self):
        #define test command
        test_command = 'ls'
        #call run command
        output, err = run_command(test_command)
        #check there is output and no error
        self.assertIsNotNone(output)
        self.assertIsNone(err)

    def test_get_list_split_files(self):
        #create test split files
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        for i in range(0, 5):
            output_file = open(os.path.join(self.output_dir, self.output_template + str(i)), 'w', newline='')
            writer = csv.writer(output_file, delimiter=',')
            for n in range(1, 6):
                row = ['Row' + str(n), 'fdsa', 'asdf']
                writer.writerow(row)
            output_file.close()
        output_list = get_list_split_files(self.output_template, self.output_dir)
        for entry in output_list:
            self.assertTrue(self.output_template in entry[0])
            self.assertEqual(entry[1], 5)
            self.assertEqual(entry[2], entry[1] * int(entry[0][-1]) + 1)
        #cleanup
        shutil.rmtree(self.output_dir)
