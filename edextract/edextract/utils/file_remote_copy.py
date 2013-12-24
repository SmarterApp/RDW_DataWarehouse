'''
Created on Nov 7, 2013

@author: tosako
'''
import os
import subprocess
from edextract.exceptions import RemoteCopyError, NotForWindowsException
from edextract.settings.config import Config, get_setting
import sys

mswindows = (sys.platform == "win32")


def copy(filename, hostname, tenant, gatekeeper, sftp_username, private_key_file, binaryfile='sftp'):
    if mswindows:
        raise NotForWindowsException('sftp remote copy cannot be served for Windows users')

    sftp_command_line = [binaryfile, '-b', '-']
    if private_key_file is not None:
        sftp_command_line += ['-oIdentityFile=' + private_key_file]
    sftp_command_line.append(sftp_username + '@' + hostname)
    remote_base_dir = get_setting(Config.PICKUP_ROUTE_BASE_DIR)
    proc = subprocess.Popen(sftp_command_line, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    proc.stdin.write(bytes('-mkdir ' + remote_base_dir + '\n', 'UTF-8'))
    proc.stdin.write(bytes('-mkdir ' + os.path.join(remote_base_dir, tenant) + '\n', 'UTF-8'))
    destination_dir = os.path.join(remote_base_dir, tenant, gatekeeper)
    proc.stdin.write(bytes('-mkdir ' + destination_dir + '\n', 'UTF-8'))
    final_destination_file = os.path.join(destination_dir, os.path.basename(filename))
    tmp_destination_file = final_destination_file + '.partial'
    # copy from local to remote
    proc.stdin.write(bytes('put ' + filename + ' ' + tmp_destination_file + '\n', 'UTF-8'))
    proc.stdin.write(bytes('chmod 600 ' + tmp_destination_file + '\n', 'UTF-8'))
    proc.stdin.write(bytes('rename ' + tmp_destination_file + ' ' + final_destination_file + '\n', 'UTF-8'))
    proc.stdin.close()
    proc.wait(timeout=10)
    status = proc.returncode
    if status != 0:
        raise RemoteCopyError(proc.stderr.read().decode())
