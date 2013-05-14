__author__ = 'abrien'

import os
import udl2_util.file_util as file_util
import time

ORIGINAL_FILE = 'original_file'
SPLIT_FILES = 'split_files'

def create_directory_structure_for_file_history(history_directory_path, landing_zone_file_path):
    '''
    This creates the entire directory structure within our history zone for the landing_zone_file.
    It will create a subdirectory of the history zone named after the landing_zone_file.
    Within this subdirectory will be 2 other subdirectories: original_file and split_files.
    original_file will contain the file initially uploaded by the user (in the landing_zone)
    split_files will contain the split_files created by W_split_files

    @param history_directory_path: Path to the history zone.
    @type history_directory_path: str

    @param landing_zone_file_path: Path to the original file in the landing_zone
    @type landing_zone_file_path: str
    '''
	try:
    	root_history_directory_for_file = create_root_history_directory_for_file(history_directory_path, landing_zone_file_path)
	    original_file_directory = create_original_file_directory(root_history_directory_for_file)
	    if os.path.exists(landing_zone_file_path):
	        print("I am the cleanup worker, I am about to clean up the zones directory.")
	        start = time.time()
	        file_util.move_file_and_confirm(landing_zone_file_path, original_file_directory)
	        end = time.time()
	        elapsed = end - start
	        print('I am the cleanup worker.  Cleaning the zones directory took %.3f seconds to complete.' % elapsed)
	    split_files_directory = create_split_files_directory(root_history_directory_for_file)
	except:
		pass
    # move_split_files_from_work_zone(split_files_directory)


def create_root_history_directory_for_file(history, csv_file):
    '''
    This function creates the subdirectory within the history zone for csv_file (if it doesn't already exist).
    It uses the name of csv_file as the directory name

    @param history: path to the history zone
    @type history: str

    @param csv_file: path to the file in the landing zone. Used to name the subdirectory within the work zone.
    @type csv_file: str

    @return: The path to the newly created subdirectory
    @rtype: str
    '''
    file_name = file_util.extract_file_name(csv_file)
    file_history_dir = os.path.join(history, file_name)
    if not os.path.exists(file_history_dir):
		os.makedirs(file_history_dir)
    return file_history_dir


def create_original_file_directory(file_history):
    '''
    Given the path to a file's history zone entry, this function creates a subdirectory called original_file.
    This directory will hold the file initially uploaded by the user (found in the landing zone)

    @param file_history: Path to a file's history zone entry.
    @type file_history: str

    @return: The path to newly created 'original_file' directory
    @rtype: str
    '''
    original_file_dir = os.path.join(file_history, ORIGINAL_FILE)
    if not os.path.exists(original_file_dir):
		os.makedirs(original_file_dir)
    return original_file_dir


def create_split_files_directory(root_file_history_dir):
    '''
    Given a file's history entry, this function creates a subdirectory for the split files (found in the work zone)

    @param root_file_history_dir: the path to the history zone entry for a specific file
    @type root_file_history_dir: str

    @return: the path to the split_files directory
    @rtype: str
    '''
    split_files_directory = os.path.join(root_file_history_dir, SPLIT_FILES)
    if not os.path.exists(split_files_directory):
        os.makedirs(split_files_directory)
    return split_files_directory
