'''
Created on Aug 11, 2014

@author: tosako
'''
import os
import csv


def file_writer(path, data, mode=0o700):
    # create directory
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(str.encode(data) if type(data) is str else data)
        written = True
    if os.path.exists(path):
        os.chmod(path, mode)
    return written if written else False


def csv_file_writer(csv_file_path, data, mode=0o700):
    # create directory
    os.makedirs(os.path.dirname(csv_file_path), mode=mode, exist_ok=True)
    with open(csv_file_path, 'w', newline='') as csv_out:
        csv_writer = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(data)
        csv_out.close()
        written = True
    if os.path.exists(csv_file_path):
        os.chmod(csv_file_path, mode)
    return written if written else False
