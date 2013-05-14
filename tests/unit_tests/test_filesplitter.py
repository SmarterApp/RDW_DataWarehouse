import unittest
import os
from filesplitter import file_splitter
import shutil
import csv

class Test(unittest.TestCase):
	
	def setUp(self):
		#define test file name and directory
		self.test_output_path = 'this/is/test/'
		self.test_file_name = 'test.csv'
		self.output_dir = 'testsplit/'
		self.output_template = 'split_part_'

	def test_create_output_dest(self):
		#if directory exists, delete it
		base =  os.path.splitext(os.path.basename(self.test_file_name))[0]
		root = self.test_output_path.split('/')[0] + '/'
		output_dir = os.path.join(self.test_output_path,base)
		if os.path.exists(output_dir): 
			shutil.rmtree(root)
		#call function to create output destination
		template,dir = file_splitter.create_output_destination(self.test_file_name,self.test_output_path)
		#check if directory created correctly
		assert os.path.exists(output_dir)
		assert template == 'test_part_'
		#clean up test directory
		shutil.rmtree(root)
		
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
		if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)
		for i in range(0,5):
			output_file = open(os.path.join(self.output_dir,self.output_template+str(i)), 'w', newline = '')
			writer = csv.writer(output_file,delimiter=',')
			for n in range(1,6):
				row = ['Row'+str(n),'fdsa','asdf']
				writer.writerow(row)
			output_file.close()	
		output_list = file_splitter.get_list_split_files(self.output_template,self.output_dir)
		for entry in output_list:
			assert self.output_template in entry[0]
			assert entry[1] == 5
			assert entry[2] == entry[1] * int(entry[0][-1]) + 1
		#cleanup
		shutil.rmtree(self.output_dir)
