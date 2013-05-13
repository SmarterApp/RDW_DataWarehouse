import unittest
import os
from filesplitter import file_splitter
import shutil
import csv

class Test(unittest.TestCase):

	def test_create_output_dest(self):
		#define test file name and directory
		test_file_name = 'test.csv'
		test_output_path = 'this/is/test/'
		#if directory exists, delete it
		output_dir = os.path.join(test_output_path,'test')
		if os.path.exists(output_dir): shutil.rmtree('this/')
		#call function to create output destination
		template,dir = file_splitter.create_output_destination(test_file_name,test_output_path)
		#check if directory created correctly
		assert os.path.exists(output_dir)
		assert template == 'test_part_'
		#clean up test directory
		shutil.rmtree('this/')
		
	def test_run_command(self):
		#define test command
		test_command = 'ls'
		#call run command
		output,err = file_splitter.run_command(test_command)
		#check there is output and no error
		assert output
		assert err is None
		
	def test_get_list_split_files(self):
		#create test split files
		outputdir = 'testsplit/'
		if not os.path.exists(outputdir): os.makedirs(outputdir)
		output_template = 'split_part_'
		for i in range(0,5):
			output_file = open(os.path.join(outputdir,output_template+str(i)), 'w', newline = '')
			writer = csv.writer(output_file,delimiter=',')
			for n in range(1,6):
				row = ['Row'+str(n),'fdsa','asdf']
				writer.writerow(row)
			output_file.close()	
		output_list = file_splitter.get_list_split_files(output_template,outputdir)
		for entry in output_list:
			assert output_template in entry[0]
			assert entry[1] == 5
			assert entry[2] == entry[1] * int(entry[0][-1]) + 1
