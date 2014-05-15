__author__ = 'sravi'

import os
import threading
import fnmatch
import subprocess
from edcore.watch.constants import WatcherConstants as Const


class FileUtil:

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size if os.path.exists(filename) else None

    @staticmethod
    def file_contains_hash(file, file_hash):
        with open(file) as f:
            if file_hash in f.read():
                return True
        return False

    @staticmethod
    def get_complement_file_name(file):
        if fnmatch.fnmatch(file, '*' + Const.CHECKSUM_FILE_EXTENSION):
            # return corresponding source file path
            return file.strip(Const.CHECKSUM_FILE_EXTENSION)
        else:
            # return corresponding checksum file path
            return ''.join([file, Const.CHECKSUM_FILE_EXTENSION])

    @staticmethod
    def get_file_tenant_and_user_name(file, base_path):
        file_rel_path = os.path.relpath(file, base_path)
        file_path_splits = file_rel_path.split(os.sep)
        if len(file_path_splits) > 2:
            # return tenant and tenant username
            return file_path_splits[0], file_path_splits[1]
        return None, None


class SendFileUtil:

    @staticmethod
    def remote_transfer_file(source_file, hostname, remote_base_dir, file_tenantname,
                             file_username, sftp_username, private_key_file, timeout=1800):
        print(source_file, hostname, remote_base_dir, file_tenantname, file_username, sftp_username, private_key_file)
        sftp_command_line = ['sftp', '-b', '-']
        if private_key_file is not None:
            sftp_command_line += ['-oIdentityFile=' + private_key_file]
        sftp_command_line.append(sftp_username + '@' + hostname)
        proc = subprocess.Popen(sftp_command_line, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        proc.stdin.write(bytes('-mkdir ' + remote_base_dir + '\n', 'UTF-8'))
        proc.stdin.write(bytes('-mkdir ' + os.path.join(remote_base_dir, file_tenantname) + '\n', 'UTF-8'))
        destination_dir = os.path.join(remote_base_dir, file_tenantname, file_username)
        proc.stdin.write(bytes('-mkdir ' + destination_dir + '\n', 'UTF-8'))
        final_destination_file = os.path.join(destination_dir, os.path.basename(source_file))
        tmp_destination_file = final_destination_file + '.partial'
        # copy from local to remote
        proc.stdin.write(bytes('put ' + source_file + ' ' + tmp_destination_file + '\n', 'UTF-8'))
        proc.stdin.write(bytes('chmod 600 ' + tmp_destination_file + '\n', 'UTF-8'))
        proc.stdin.write(bytes('rename ' + tmp_destination_file + ' ' + final_destination_file + '\n', 'UTF-8'))
        proc.stdin.close()
        proc.wait(timeout=timeout)
        status = proc.returncode
        return status


def set_interval(interval):
    """Decorator to schedule method to run after every interval

    The method will be run in a separate thread and will run until explicitly stopped by the main thread
    To stop the scheduled method call set() on the returned event object

    :param interval: interval in seconds
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)
            t = threading.Thread(target=loop)
            t.daemon = True
            t.start()
            return stopped
        return wrapper
    return decorator
