'''
Created on Jul 21, 2014

@author: tosako
'''
import os
import argparse


def metadata_generator(dir_path, metadata_filename='.metadata', recursive=True, force=True, verbose=False):
    if os.path.isdir(dir_path):
        if verbose:
            print('seaching directory: [' + dir_path + ']')
        directories = [os.path.join(dir_path, d) for d in os.listdir(dir_path)]
        if recursive:
            for directory in directories:
                if os.path.isdir(directory):
                    metadata_generator(directory, metadata_filename=metadata_filename, recursive=recursive, force=force, verbose=verbose)
        fileMeatadata = FileMetadata(dir_path, metadata_filename=metadata_filename)
        fileMeatadata.write()
        if verbose:
            print('generated metadata: [' + fileMeatadata.name + ']')
    else:
        print('[' + dir_path + '] is not directory')


class FileMetadata():
    '''
    create file metadata to each directories and recursivly.
    /path/.metadata
    base_file_name:file_size:file_creation_date
    '''
    def __init__(self, dir_path, metadata_filename='.metadata', force=True):
        self.__path = os.path.abspath(dir_path)
        self.__metadata_filename = metadata_filename
        self.__dirs = []
        self.__files = []
        self.__force = force
        self._read_files()

    def _read_files(self):
        '''
        read only files
        '''
        if not self.__force and os.path.exists(os.path.join(self.__path, self.__metadata_filename)):
            return
        files = [os.path.join(self.__path, f) for f in os.listdir(self.__path)]
        for file in files:
            basename = os.path.basename(file)
            if os.path.isfile(file):
                if not basename.startwith('.') and basename != self.__metadata_filename:
                    self.__files.append(FileMetadata.FileInfo(file))
            elif os.path.isdir(file) and not basename.startwith('.'):
                self.__dirs.append(FileMetadata.DirInfo(file))

    @property
    def name(self):
        return os.path.join(self.__path, self.__metadata_filename)

    @staticmethod
    def _format(file, delimiter=':'):
        return file.type + delimiter + file.name + delimiter + str(file.size) + delimiter + str(file.time)

    def write(self):
        def _write(fd, info):
            for d in sorted(info, key=lambda x: x.name):
                if fd.tell() > 0:
                    fd.write('\n')
                fd.write(self._format(d))
        if self.__files or self.__dirs:
            with open(self.name, 'w') as f:
                _write(f, self.__dirs)
                _write(f, self.__files)
            
    class DirInfo():
        def __init__(self, dir_path, metadata_filename='.metadata', delimiter=':'):
            self.__dir_path = dir_path
            stat_info = os.stat(dir_path)
            self.__last_c_time = stat_info.st_ctime
            self.__metadata_filename = metadata_filename
            self.__size = self.get_size(delimiter=delimiter)

        def read_metadata(self, delimiter=':'):
            metadata = []
            metadata_file = os.path.join(self.__dir_path, self.__metadata_filename)
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    for line in f:
                        metadata.append(line.strip().split(':'))
            return metadata

        def get_size(self, delimiter=':'):
            size = 0
            metadata = self.read_metadata(delimiter=delimiter)
            for m in metadata:
                size += int(m[2])
            return size

        @property
        def name(self):
            return os.path.basename(self.__dir_path)

        @property
        def size(self):
            return self.__size

        @property
        def time(self):
            return self.__last_c_time

        @property
        def type(self):
            return 'd'

    class FileInfo():
        def __init__(self, filename):
            self.__filename = filename
            stat_info = os.stat(filename)
            self.__last_c_time = stat_info.st_ctime
            self.__file_size = stat_info.st_size

        @property
        def name(self):
            return os.path.basename(self.__filename)

        @property
        def size(self):
            return self.__file_size

        @property
        def time(self):
            return self.__last_c_time

        @property
        def type(self):
            return 'f'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Metadata generator')
    parser.add_argument('-d', '--dir', help='directory to read', required=True)
    parser.add_argument('-r', '--recursive', help='generate metadata recursively', action='store_true', default=True)
    parser.add_argument('-m', '--metadata', help='metadata filename', default='.metadata')
    parser.add_argument('-f', '--force', help='force generate metadata if exists', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
    args = parser.parse_args()
    __dir = args.dir
    __recursive = args.recursive
    __metadata = args.metadata
    __verbose = args.verbose
    __force = args.force

    metadata_generator(__dir, metadata_filename=__metadata, recursive=__recursive, force=__force, verbose=__verbose)
