'''
Created on Jul 22, 2014

@author: tosako
'''
import os
import logging


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
        return filesize

    def _load_metadata(self, filepath):
        metadata_file = os.path.join(os.path.dirname(filepath), self.__metadata_filename)
        if os.path.exists(metadata_file) and metadata_file not in self.__metadata_tracker:
            self.__metadata_tracker.add(metadata_file)
            with open(metadata_file, 'r') as f:
                logging.info('opening metadata[' + metadata_file + ']')
                directory = os.path.dirname(metadata_file)
                for l in f:
                    metadata = l.strip().split(self.__delimiter)
                    self.__metadata[os.path.join(directory, metadata[1])] = int(metadata[2])
                logging.info('closing metadata[' + metadata_file + ']')
            if self.__metadata.get(filepath) is None:
                self.__metadata[filepath] = os.stat(filepath).st_size
        else:
            self.__metadata[filepath] = os.stat(filepath).st_size
            if metadata_file not in self.__metadata_tracker:
                self.__metadata_tracker.add(metadata_file)
                logging.info('metadata not found[' + metadata_file + ']')
