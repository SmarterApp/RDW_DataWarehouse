__author__ = 'abrien'

import os
import shutil

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
        #print('ERROR while copying file (%s) to directory (%s)' % (source_file, target_directory))
        #print(e)
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
        # print('ERROR removing file (%s)' % (target_file,))
        # print('Aforementioned file still exists in original directory.')
        print(e)


def move_file_and_confirm(file_to_move, target_directory):
    '''
    This function moves a file to a different directory.
    If successful in doing this, it then removes the file from the original directory completely.

    @param file_to_move: The path to the landing zone file that will be moved to the history zone.
    @type file_to_move: str

    @param target_directory: The path to the file's original_file directory.  This is where the file will be moved.
    @type target_directory: str
    '''
    copied_successfully = copy_file(file_to_move, target_directory)
    if copied_successfully:
        remove_file(file_to_move)


def abs_path_join(*args):
    """Performs os.path.join on all args, then returns the absolute path

    :param args: any amount of args
    :type args: strings
    """
    if args:
        full_path = ''
        for arg in args:
            full_path = os.path.join(full_path, arg)
        return os.path.abspath(full_path)