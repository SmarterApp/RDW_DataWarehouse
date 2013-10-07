import os
import subprocess
import csv
import math
import argparse
import datetime
import logging

logger = logging.getLogger(__name__)


def __is_file_exists(file_to_decrypt):
    '''
    check if file exists and readable
    '''
    return os.path.isfile(file_to_decrypt) and os.access(file_to_decrypt, os.R_OK)


def __is_valid__file(file_to_decrypt):
    '''
    Basic file validation checks before decrypting
    '''
    valid=False
    if __is_file_exists(file_to_decrypt):
        valid=True
        print("File exists and is readable -- %s " % file_to_decrypt)
    else:
        print("File missing or un-readable -- %s " % file_to_decrypt)        

    return valid


def __decrypt_file_contents(file_to_decrypt, destination_dir):
    '''
    verify signature, decrypt and write the decrypted file to the destination directory
    '''
    return None


def decrypt_file(file_to_decrypt, destination_dir):
    '''
    Verify and Decrypt the file after needed validations
    '''
    if not __is_valid__file(file_to_decrypt):
        raise Exception('Invalid source file -- %s' % file_to_decrypt)

    __decrypt_file_contents(file_to_decrypt, destination_dir)

    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file decrypter args')
    parser.add_argument('-i', '--input', dest="file_to_decrypt", help='file_to_expand')
    parser.add_argument('-o', '--output', dest="destination_dir", default='.', help='output directory')

    args = parser.parse_args()
    print("Input file is: " + args.file_to_decrypt)
    if args.destination_dir:
        print("Decrypt files to: " + args.destination_dir)

    decrypt_file(args.file_to_decrypt, args.destination_dir)