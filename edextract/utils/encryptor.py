'''
Created on Nov 4, 2013

@author: tosako
'''
import subprocess
import io
import threading
import os


class Encryptor:
    '''
    GnuPG command wrapper class.
    This wrapper class increases I/O performance between data input and gpg program as well as I/O between gpg program and output file.
    '''
    BUFFER_SIZE = 1024

    def __init__(self, output_file=None, recipient=None, compress_level='9', binaryfile='gpg'):
        # GPG process
        self.__proc = subprocess.Popen([binaryfile, '--encrypt', '--recipient', recipient, '--compress-level', compress_level], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # input buffer buffer size is 1k
        reader, writer = os.pipe()

        self.__bufferedreader = io.BufferedReader(io.FileIO(reader, 'r'), buffer_size=Encryptor.BUFFER_SIZE)
        self.__bufferedwriter = io.BufferedWriter(io.FileIO(writer, 'w'), buffer_size=Encryptor.BUFFER_SIZE)

        self.__input_thread = threading.Thread(target=self.__pipe_data, args=(self.__bufferedreader, self.__proc.stdin, 'reader'))
        self.__input_thread.setDaemon(True)
        self.__input_thread.start()

        # output buffer buffer size is 1k
        output_fileio = io.BufferedWriter(io.FileIO(output_file, mode='w'), buffer_size=Encryptor.BUFFER_SIZE)
        self.__output_thread = threading.Thread(target=self.__pipe_data, args=(self.__proc.stdout, output_fileio, 'writer'))
        self.__output_thread.setDaemon(True)
        self.__output_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, tb):
        self.close()

    def encrypt(self, data):
        '''
        Encrypt data from stream.
        '''
        self.__bufferedwriter.write(data.encode())

    def close(self):
        '''
        close stream. Destructor also call this function before Object is destroied.
        '''
        if not self.__bufferedwriter.closed:
            self.__bufferedwriter.flush()
            self.__bufferedwriter.close()
            self.__input_thread.join()
            self.__output_thread.join()

    @staticmethod
    def __pipe_data(input_stream, output_stream, name):
        while True:
            data = input_stream.read(Encryptor.BUFFER_SIZE)
            if not data:
                break
            output_stream.write(data)
        input_stream.flush()
        input_stream.close()
        output_stream.flush()
        output_stream.close()
