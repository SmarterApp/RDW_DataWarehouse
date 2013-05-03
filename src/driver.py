from __future__ import absolute_import
import udl2.W_file_splitter
import random


def main():
    file_name = str(int(random.random() * 1000000)) + '.csv'    
    udl2.W_file_splitter.task.apply_async(['process file ' + file_name], queue='Q_files_to_be_split')


if __name__ == '__main__':
    main()
