__author__ = 'abrien'

import os
import shutil

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
    root_history_directory_for_file = create_root_history_directory_for_file(history_directory_path, landing_zone_file_path)
    original_file_directory = create_original_file_directory(root_history_directory_for_file)
    if os.path.exists(landing_zone_file_path):
        move_file_from_landing_zone(landing_zone_file_path, original_file_directory)
    split_files_directory = create_split_files_directory(root_history_directory_for_file)
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
    file_name = extract_file_name(csv_file)
    file_history_dir = os.path.join(history, file_name)
    if not os.path.exists(file_history_dir):
        os.makedirs(file_history_dir)
    return file_history_dir


def extract_file_name(file_path):
    '''
    Given a path to a file, this function removes the path and the extension, simply returning the filename.

    @param file_path: Path to the file whose name will be extracted
    @type file_path: str

    @return: the file's name
    @rtype: str
    '''
    file_name_and_ext = os.path.basename(file_path)
    file_name = os.path.splitext(file_name_and_ext)[0]
    return file_name


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


def move_file_from_landing_zone(landing_zone_file, original_file_directory):
    '''
    This function moves a landing zone file to it's 'original_file' directory in the history zone.
    If successful in doing this, it then removes the file from the landing zone completely.

    @param landing_zone_file: The path to the landing zone file that will be moved to the history zone.
    @type landing_zone_file: str

    @param original_file_directory: The path to the file's original_file directory.  This is where the file will be moved.
    @type original_file_directory: str
    '''
    copied_successfully = copy_file(landing_zone_file, original_file_directory)
    if copied_successfully:
        remove_file(landing_zone_file)


def copy_file(source_file, target_directory):
    '''
    This function moves the source file to the target directory by wrapping shutil.copy2(...)
    If an error occurs during the copy process, some custom error printing will take place.
    It will return True if the move completed successfully and False otherwise.

    @param source_file: The path to the file that will be copied over to the target directory.
    @type source_file: str

    @param target_directory: The path to the directory that will hold the source_file
    @type target_directory: str

    @return: True if copy completed successfully, False if anything went wrong
    @rtype: bool
    '''
    try:
        shutil.copy2(source_file, target_directory)
        return True
    except IOError as e:
        print('ERROR while copying file (%s) to directory (%s)' % (source_file, target_directory))
        print(e)
        return False


def remove_file(target_file):
    '''
    This function removes target_file by wrapping os.remove()

    @param target_file: The file to remove
    @type target_file: str
    '''
    try:
        os.remove(target_file)
    except OSError as e:
        print('ERROR removing file (%s)' % (target_file,))
        print('Aforementioned file still exists in original directory.')
        print(e)


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