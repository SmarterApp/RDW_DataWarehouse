# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Jul 22, 2014

@author: tosako
'''
import os
import logging
import fcntl
import fnmatch


logger = logging.getLogger('edextract')


class MetadataReader():
    '''
    Metadata raeader
    filetype:filename:filesize:last_mod_timestamp
    '''
    def __init__(self, metadata_filename='.metadata', delimiter=':'):
        self.__metadata = {}
        self.__metadata_tracker = set()
        self.__metadata_filename = metadata_filename
        self.__delimiter = delimiter

    def get_size(self, filepath):
        filesize = self.__metadata.get(filepath)
        if filesize is None:
            self._load_metadata(filepath)
            filesize = self.__metadata.get(filepath)
            if filesize is None and os.path.exists(filepath):
                filesize = os.stat(filepath).st_size
                self.__metadata[filepath] = filesize
        return filesize if filesize is not None else -1

    def get_files(self, file_pattern):
        self._load_metadata(file_pattern)
        files = []
        _dir, _base = os.path.split(file_pattern)
        for f in self.__metadata.keys():
            if fnmatch.fnmatch(os.path.basename(f), _base):
                files.append(f)
        return files

    def _load_metadata(self, filepath):
        metadata_file = os.path.join(os.path.dirname(filepath), self.__metadata_filename)
        if os.path.exists(metadata_file) and metadata_file not in self.__metadata_tracker:
            self.__metadata_tracker.add(metadata_file)
            with open(metadata_file, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                logging.info('opening metadata[' + metadata_file + ']')
                directory = os.path.dirname(metadata_file)
                for l in f:
                    metadata = l.strip().split(self.__delimiter)
                    self.__metadata[os.path.join(directory, metadata[1])] = int(metadata[2])
                logging.info('closing metadata[' + metadata_file + ']')
                fcntl.flock(f, fcntl.LOCK_UN)
        else:
            if metadata_file not in self.__metadata_tracker:
                self.__metadata_tracker.add(metadata_file)
                logging.info('metadata not found[' + metadata_file + ']')
