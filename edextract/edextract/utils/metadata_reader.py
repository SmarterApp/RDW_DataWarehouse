'''
Created on Jul 22, 2014

@author: tosako
'''
import os


class MetadataReader():

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
                directory = os.path.dirname(metadata_file)
                for l in f:
                    metadata = l.strip().split(self.__delimiter)
                    self.__metadata[os.path.join(directory, metadata[1])] = int(metadata[2])
            if self.__metadata.get(filepath) is None:
                self.__metadata[filepath] = os.stat(filepath).st_size
        else:
            self.__metadata[filepath] = os.stat(filepath).st_size
