'''
Created on Mar 13, 2013

@author: swimberly
'''

import unittest
import os

from mock import MagicMock

from DataGeneration.dataload import load_data


class TestDataLoad(unittest.TestCase):

    def setUp(self):
        load_data.system = MagicMock(side_effect=self.system_mock)
        load_data.get_table_order = MagicMock(side_effect=self.get_table_order_mock)
        load_data.setup_pg_passwd_file = MagicMock(return_value={'PGPASSFILE': 'filename'})
        os.remove = MagicMock()
        self.input_args = {
            'schema': 'schema',
            'passwd': 'passwd',
            'csvdir': 'csvdir',
            'database': 'database',
            'host': 'host',
            'user': 'user',
            'port': '1234',
            'truncate': False
        }

    def test_load_data(self):
        ''' Test load_data '''

        load_data.load_data_main(self.input_args['csvdir'], self.input_args['host'], self.input_args['database'], self.input_args['user'], self.input_args['passwd'], self.input_args['schema'], self.input_args['port'], self.input_args['truncate'])

        self.input_args['truncate'] = True
        load_data.load_data_main(self.input_args['csvdir'], self.input_args['host'], self.input_args['database'], self.input_args['user'], self.input_args['passwd'], self.input_args['schema'], self.input_args['port'], self.input_args['truncate'])

        load_data.system = MagicMock(side_effect=self.system_mock2)

        load_data.get_table_order = MagicMock(side_effect=self.get_table_order_mock2)
        load_data.load_data_main(self.input_args['csvdir'], self.input_args['host'], self.input_args['database'], self.input_args['user'], self.input_args['passwd'], self.input_args['schema'], self.input_args['port'], self.input_args['truncate'])

    def get_table_order_mock(self, *args, **kwargs):
        ''' Mock of get_table_order'''
        return ['dim_fake', 'dim_fake2', 'dim_fake3']

    def get_table_order_mock2(self, *args, **kwargs):
        ''' Mock of get_table_order'''
        return ['dim_fake', 'dim_fake2']

    def system_mock(self, *args, **kwargs):
        '''
        Method to use instead of the System method defined in the code
        Returns true if the input params are are valid.
        False otherwise
        '''
        for i in range(len(args)):
            # Check that the first argument does not contain spaces
            arg = args[i]
            if i == 0:
                self.assertNotIn(' ', arg)
            # check for spaces before the argument following a flag.
            if arg[0] == '-' and len(arg) > 2:
                self.assertNotEqual(' ', arg[2])

        if args[0] == 'ls':
            return b'dim_fake.csv\ndim_fake2.csv\ndim_fake3.csv\n'

    def system_mock2(self, *args, **kwargs):
        '''
        Method to use instead of the System method defined in the code
        Returns true if the input params are are valid.
        False otherwise
        '''
        for i in range(len(args)):
            # Check that the first argument does not contain spaces
            arg = args[i]
            if i == 0:
                self.assertNotIn(' ', arg)
            # check for spaces before the argument following a flag.
            if arg[0] == '-' and len(arg) > 2:
                self.assertNotEqual(' ', arg[2])

        if args[0] == 'ls':
            return b'dim_fake.csv\ndim_fake2.csv\n'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
