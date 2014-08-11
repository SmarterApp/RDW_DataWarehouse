'''
Created on Jul 21, 2014

@author: tosako
'''
import os
import argparse


DIRECTORY = 'd'
FILE = 'f'

def metadata_generator_top_down(dir_path, metadata_filename='.metadata', recursive=True, force=True, verbose=False):
    if os.path.isdir(dir_path):
        if verbose:
            print('seaching directory: [' + dir_path + ']')
        directories = [os.path.join(dir_path, d) for d in os.listdir(dir_path)]
        if recursive:
            for directory in directories:
                if os.path.isdir(directory):
                    metadata_generator_top_down(directory, metadata_filename=metadata_filename, recursive=recursive, force=force, verbose=verbose)
        fileMeatadata = FileMetadata(dir_path, metadata_filename=metadata_filename)
        fileMeatadata.read_files()
        fileMeatadata.write()
        if verbose:
            print('generated metadata: [' + fileMeatadata.name + ']')
    else:
        print('[' + dir_path + '] is not directory')


def metadata_generator_bottom_up(file_path, metadata_filename='.metadata', recursive=True, verbose=False):
    dirname = os.path.dirname(file_path)
    updating_metadata = os.path.join(dirname, metadata_filename)
    if os.path.isfile(updating_metadata):
        if os.path.exists(file_path):
            dir_path = os.path.dirname(file_path)
            fileMetadata = FileMetadata(dir_path, metadata_filename=metadata_filename)
            fileMetadata.load_metadata()
            fileMetadata.read_file(file_path)
            fileMetadata.write()
        if recursive:
            metadata_generator_bottom_up(dirname, metadata_filename=metadata_filename, recursive=recursive, verbose=verbose)
        

class FileMetadata():
    '''
    create file metadata to each directories and recursivly.
    /path/.metadata
    base_file_name:file_size:file_creation_date
    '''
    def __init__(self, dir_path, metadata_filename='.metadata'):
        self.__path = os.path.abspath(dir_path)
        self.__metadata_filename = metadata_filename
        self.__dirs = {}
        self.__files = {}

    def load_metadata(self, delimiter=':'):
        def setMetadata(metainfo):
            metainfo.name = meta[1]
            metainfo.size = meta[2]
            metainfo.time = meta[3]
            return metainfo
        metadata_filepath = os.path.join(self.__path, self.__metadata_filename)
        if os.path.isfile(metadata_filepath):
            with open(metadata_filepath) as f:
                for l in f:
                    meta = l.strip().split(delimiter)
                    if meta[0] == DIRECTORY:
                        dirinfo = FileMetadata.DirInfo()
                        metainfo = setMetadata(dirinfo)
                        self.__dirs[metainfo.name] = metainfo
                    elif meta[0] == FILE:
                        fileinfo = FileMetadata.FileInfo()
                        metainfo = setMetadata(fileinfo)
                        self.__files[metainfo.name] = metainfo

    def read_files(self, force=True):
        '''
        read only files
        '''
        if not force and os.path.exists(os.path.join(self.__path, self.__metadata_filename)):
            return
        files = [os.path.join(self.__path, f) for f in os.listdir(self.__path)]
        for file in files:
            self.read_file(file)

    def read_file(self, file):
        '''
        read a file
        '''
        basename = os.path.basename(file)
        if os.path.isfile(file):
            if not basename.startswith('.') and basename != self.__metadata_filename:
                fileinfo = FileMetadata.FileInfo()
                fileinfo.read_file_info(file)
                self.__files[basename] = fileinfo
        elif os.path.isdir(file) and not basename.startswith('.'):
            dirinfo = FileMetadata.DirInfo()
            dirinfo.read_dir_info(file)
            self.__dirs[basename] = dirinfo

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
                _write(f, list(self.__dirs.values()))
                _write(f, list(self.__files.values()))
            
    class DirInfo():
        def __init__(self):
            pass

        def read_dir_info(self, dir_path, metadata_filename='.metadata', delimiter=':'):
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
                        metadata.append(line.strip().split(delimiter))
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

        @name.setter
        def name(self, value):
            self.__dir_path = value

        @property
        def size(self):
            return self.__size

        @size.setter
        def size(self, value):
            self.__size = value

        @property
        def time(self):
            return self.__last_c_time

        @time.setter
        def time(self, value):
            self.__last_c_time = value

        @property
        def type(self):
            return DIRECTORY

    class FileInfo():
        def __init__(self):
            pass

        def read_file_info(self, filename):
            self.__filename = filename
            stat_info = os.stat(filename)
            self.__last_c_time = stat_info.st_ctime
            self.__file_size = stat_info.st_size

        @property
        def name(self):
            return os.path.basename(self.__filename)

        @name.setter
        def name(self, value):
            self.__filename = value

        @property
        def size(self):
            return self.__file_size

        @size.setter
        def size(self, value):
            self.__file_size = value

        @property
        def time(self):
            return self.__last_c_time

        @time.setter
        def time(self, value):
            self.__last_c_time = value

        @property
        def type(self):
            return FILE


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Metadata generator')
    # parser.add_argument('-n', '--dir', help='directory to read', required=True)
    parser.add_argument('-p', '--path', help='directory/file path to read', default='/tmp/a/c/f')
    parser.add_argument('-r', '--recursive', help='generate metadata recursively', action='store_true', default=True)
    parser.add_argument('-m', '--metadata', help='metadata filename', default='.metadata')
    parser.add_argument('-f', '--force', help='force generate metadata if exists', action='store_true', default=False)
    parser.add_argument('-u', '--up', help='update metadat from bottom to up', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
    args = parser.parse_args()
    __path = args.path
    __recursive = args.recursive
    __metadata = args.metadata
    __verbose = args.verbose
    __force = args.force
    __up = args.up

    if __up:
        metadata_generator_top_down(__path, metadata_filename=__metadata, recursive=__recursive, force=__force, verbose=__verbose)
    else:
        metadata_generator_bottom_up(__path, metadata_filename=__metadata, recursive=__recursive, verbose=__verbose)
