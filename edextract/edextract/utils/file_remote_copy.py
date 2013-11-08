'''
Created on Nov 7, 2013

@author: tosako
'''
import os
import subprocess


REMOTE_BASE_DIR = 'route'


def copy(filename, hostname, tenant, request_username, sftp_username, private_key_file, binaryfile='sftp'):
    status = -1
    sftp_command_line = [binaryfile, '-b', '-']
    if private_key_file is not None:
        sftp_command_line += ['-i', private_key_file]
    sftp_command_line.append(sftp_username + '@' + hostname)
    proc = subprocess.Popen(sftp_command_line, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc.stdin.write(bytes('-mkdir ' + REMOTE_BASE_DIR + '\n', 'UTF-8'))
    proc.stdin.write(bytes('-mkdir ' + os.path.join(REMOTE_BASE_DIR, tenant) + '\n', 'UTF-8'))
    destination_dir = os.path.join(REMOTE_BASE_DIR, tenant, request_username)
    proc.stdin.write(bytes('-mkdir ' + destination_dir + '\n', 'UTF-8'))
    final_destination_file = os.path.join(destination_dir, os.path.basename(filename))
    tmp_detination_file = final_destination_file + '.partial'
    proc.stdin.write(bytes('put ' + filename + ' ' + tmp_detination_file + '\n', 'UTF-8'))
    proc.stdin.write(bytes('chmod 600 ' + tmp_detination_file + '\n', 'UTF-8'))
    proc.stdin.write(bytes('rename ' + tmp_detination_file + ' ' + final_destination_file + '\n', 'UTF-8'))
    proc.stdin.close()
    proc.wait(timeout=10)
    status = proc.returncode
    return status
