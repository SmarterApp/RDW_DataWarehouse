'''
Created on Nov 4, 2013

@author: tosako
'''
import subprocess
import io
import threading
import os


class FileEncryptor:
    '''
    GnuPG command wrapper class.
    This wrapper class increases I/O performance between data input and gpg program as well as I/O between gpg program and output file.

    how to use:
    with FileEncryptor(output_file='/tmp/encrypted_output.txt', recipient='Example User') as e:
        e.encrypt('this is first')
        e.encrypt('this is second')
    '''
    BUFFER_SIZE = 1024 * 1024

    def __init__(self, output_file, recipient, homedir=None, compress_level='9', binaryfile='gpg'):
        # GPG process
        gpg_command_lines = [binaryfile, '--encrypt', '--recipient', recipient, '--compress-level', compress_level]
        if homedir is not None:
            gpg_command_lines += ['--homedir', homedir]
        self.__proc = subprocess.Popen(gpg_command_lines, bufsize=FileEncryptor.BUFFER_SIZE,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # input buffer buffer size is 1M
        reader, writer = os.pipe()

        self.__bufferedreader = io.BufferedReader(io.FileIO(reader, 'r'), buffer_size=FileEncryptor.BUFFER_SIZE)
        self.__bufferedwriter = io.BufferedWriter(io.FileIO(writer, 'w'), buffer_size=FileEncryptor.BUFFER_SIZE)

        self.__input_thread = threading.Thread(target=self.__pipe_data, args=(self.__bufferedreader, self.__proc.stdin, 'reader'))
        self.__input_thread.setDaemon(True)
        self.__input_thread.start()

        # output buffer buffer size is 1M
        output_fileio = io.BufferedWriter(io.FileIO(output_file, mode='w'), buffer_size=FileEncryptor.BUFFER_SIZE)
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
        this method is re-usable for incoming stream data.
        '''
        self.__bufferedwriter.write(data.encode())

    def write(self, data):
        '''
        Write data to be encrypted, anything with write method that take data is a file object in python.
        :param data: data to be encrypted
        '''
        self.encrypt(data)

    def close(self):
        '''
        close stream. Destructor also call this function before Object is destroyed.
        '''
        if not self.__bufferedwriter.closed:
            self.__bufferedwriter.flush()
            self.__bufferedwriter.close()
            self.__input_thread.join()
            self.__output_thread.join()
        self.__proc.wait(timeout=15)
        status = self.__proc.returncode
        if status != 0:
            raise FileEncryptorException(self.__proc.stderr.read().decode())

    @staticmethod
    def __pipe_data(input_stream, output_stream, name):
        while True:
            data = input_stream.read(FileEncryptor.BUFFER_SIZE)
            if not data:
                break
            output_stream.write(data)
        input_stream.flush()
        input_stream.close()
        output_stream.flush()
        output_stream.close()


class FileEncryptorException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
