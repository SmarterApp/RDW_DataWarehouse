'''
Created on Nov 11, 2013

@author: tosako
'''
import os
import stat
import shutil
import syslog
import sys
import signal
import time
import atexit
import argparse
import pwd

PID_DIR = '/var/run/filerouter'
PID_FILE = 'filerouter.pid'
PROCESS_SUFFIX = '.process'
LOOP = True


class FileRouterException(Exception):
    pass


class GatekeeperException(FileRouterException):
    def __init__(self, message):
        self.__message = message

    def __repr__(self):
        return repr(self.__message)


class FileInfo():
    '''
    Given full path filename, reads tenant, gatekeeper, and filenamd
    '''
    def __init__(self, filename):
        path = filename.split(os.path.sep)
        self.__filename = path.pop()
        self.__gatekeeper = path.pop()
        self.__tenant = path.pop()

    def get_file_info(self):
        '''
        reading file directory structure and return filename, gatekeeper username, and tenant name
        '''
        return self.__filename, self.__gatekeeper, self.__tenant


def _route_for_error_file(original_file_name, route_dir, error_dir):
    '''
    Route from file in route directory to error directory
    '''
    # replace /route/ to /error/
    error_file = original_file_name.replace(os.sep + route_dir + os.sep, os.sep + error_dir + os.sep)

    # if error file already exist, delete it.
    if os.path.isfile(error_file):
        os.unlink(error_file)
    # check error directory first.  If the directory does not exist, then mkdir.
    error_dir = os.path.dirname(error_file)
    if not os.path.isdir(error_dir):
        os.makedirs(error_dir, mode=(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR), exist_ok=True)
    # move file to error directory
    os.rename(original_file_name, error_file)
    syslog.syslog(syslog.LOG_INFO, 'File moved: [{}] to [{}]'.format(original_file_name, error_file))


def _mkdir(directory, gatekeeper_uid, gatekeeper_gid):
    if not os.path.isdir(directory):
        os.makedirs(directory, mode=(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR), exist_ok=True)
        if gatekeeper_uid is not None and gatekeeper_gid is not None:
            os.chown(directory, gatekeeper_uid, gatekeeper_gid)


def _route_file_for_gatekeeper(gatekeeper_jailed_home_base, original_file_name, home_base, gatekeeper_reports_subdir, archive_dir, set_file_owner=True):
    '''
    copy file to gatekeeper account.
    '''
    # find destination file name
    # the functino will throw exception if gatekeeper account has not created or file is already existed in the acconut.
    original_file_info = FileInfo(original_file_name)
    destination_file_name = _get_destination_filename_for_gatekeeper(gatekeeper_jailed_home_base, gatekeeper_reports_subdir, original_file_info)
    destination_file_dir = os.path.dirname(destination_file_name)
    (_filename, _gatekeeper, _tenant) = original_file_info.get_file_info()
    gatekeeper_uid = None
    gatekeeper_gid = None
    if set_file_owner:
        gatekeeper_uid = pwd.getpwnam(_gatekeeper).pw_uid
        gatekeeper_gid = pwd.getpwnam(_gatekeeper).pw_gid
    _mkdir(destination_file_dir, gatekeeper_uid, gatekeeper_gid)

    # rename file to indicate that file is being copying.
    working_file = original_file_name + PROCESS_SUFFIX
    filedir, filename = os.path.split(destination_file_name)
    # create hidden file name for destination. Make invisible for gatekeeper
    hidden_to_file = os.path.join(filedir, "." + filename)
    # start copying file
    os.rename(original_file_name, working_file)
    shutil.copyfile(working_file, hidden_to_file)

    # archive file
    archive_file_name = _get_archive_filename_for_gatekeeper(home_base, archive_dir, original_file_info)
    full_archive_dir = os.path.dirname(archive_file_name)
    _mkdir(full_archive_dir, gatekeeper_uid, gatekeeper_gid)
    shutil.copyfile(working_file, archive_file_name)

    # make sure copied hidden file is readable to owner
    os.chmod(hidden_to_file, mode=(stat.S_IRUSR | stat.S_IWUSR))
    if set_file_owner:
        os.chown(hidden_to_file, gatekeeper_uid, gatekeeper_gid)
        os.chown(archive_file_name, gatekeeper_uid, gatekeeper_gid)
    # make file visible
    os.rename(hidden_to_file, destination_file_name)

    # remove file
    os.unlink(working_file)
    syslog.syslog(syslog.LOG_INFO, 'File moved: [{}] to [{}]'.format(original_file_name, destination_file_name))


def _find_files(path, suffix='.zip.gpg'):
    '''
    find "*.zip" file recursively by given base dir.
    '''
    filenames = []
    if path is not None:
        mode = os.stat(path).st_mode
        if stat.S_ISREG(mode):
            if os.path.basename(path).endswith(suffix):
                filenames.append(path)
        elif stat.S_ISDIR(mode):
            dirs = os.listdir(path)
            for file in dirs:
                filenames += _find_files(os.path.join(path, file), suffix=suffix)
    return filenames


def _get_destination_filename_for_gatekeeper(gatekeeper_jailed_home_base, gatekeeper_reports_subdir, file_info):
    '''
    copy file from router account to gatekeeper jailed account
    '''
    (filename, gatekeeper, tenant) = file_info.get_file_info()
    # check if jailed account path exist.
    gatekeeper_home_dir = os.path.join(gatekeeper_jailed_home_base, tenant, gatekeeper)
    if os.path.isdir(gatekeeper_home_dir):
        # check the file has existed already.
        destination_filename = os.path.join(gatekeeper_home_dir, gatekeeper_reports_subdir, filename)
        if os.path.isfile(destination_filename):
            # file should not be existed there.
            # failed condition
            raise GatekeeperException('File name[{}] has already existed'.format(destination_filename))
    else:
        # most likely sftp jailed account has not created.
        # failed condition
        raise GatekeeperException('Gatekeeper[{}] has not created for SFTP jailed account[{}]'.format(gatekeeper, gatekeeper_home_dir))
    return destination_filename


def _get_archive_filename_for_gatekeeper(home_base, archive_dir, fileinfo):
    '''
    compose archive filename
    '''
    (filename, gatekeeper, tenant) = fileinfo.get_file_info()
    # check if jailed account path exist.
    return os.path.join(home_base, tenant, gatekeeper, archive_dir, filename)


def file_routing(gatekeeper_jailed_home_base, gatekeeper_home_base, filerouter_jailed_home_dir, gatekeeper_reports_subdir, route_dir, error_dir, archive_dir, set_file_owner=True):
    '''
    main file routing function
    1. find routable file
    2. copy to sftp jailed account
    3. archive
    4. delete file
    '''
    filerouter_home_dir_route = os.path.join(filerouter_jailed_home_dir, route_dir)
    files = _find_files(filerouter_home_dir_route)
    for file in files:
        try:
            _route_file_for_gatekeeper(gatekeeper_jailed_home_base, file, gatekeeper_home_base, gatekeeper_reports_subdir, archive_dir, set_file_owner)
        except Exception as e:
            # failed at copy. revert filename and route file to error.
            syslog.syslog(syslog.LOG_ERR, str(e))
            _route_for_error_file(file, route_dir, error_dir)


def daemonize():
    '''
    damonize process
    '''
    # fork process first
    try:
        pid = os.fork()
    except OSError as e:
        sys.stderr.write('Cannot fork.  Failed to start the program [{}]\n'.format(e.strerror))
        sys.exit(1)
    if pid > 0:
        # bye-bye parent
        sys.exit(0)
    # hello child.
    # change working directory to root directory
    os.chdir('/')
    # creating a unique session id
    # make child process as a process group leader to prevent the child process becomes an orphan in the system
    os.setsid()
    # making sure this process has full access to the files.
    os.umask(0)

    if not os.path.isdir(PID_DIR):
        os.mkdir(PID_DIR)
    pid_file = os.path.join(PID_DIR, PID_FILE)
    if os.path.exists(pid_file):
        sys.stderr.write("File[{}] is already existed.\n".format(pid_file))
        sys.exit(1)
    # running mutual exclusion and running a single copy
    pid_fo = open(pid_file, 'w')
    pid = str(os.getegid())
    pid_fo.write(pid)
    pid_fo.close()
    atexit.register(delete_pid_file, pid_file)

    # closing standard file descriptors
    sys.stdin.flush()
    sys.stdout.flush()
    sys.stderr.flush()
    null_device = os.open(os.devnull, os.O_RDWR)
    os.dup2(null_device, sys.stdin.fileno())
    os.dup2(null_device, sys.stdout.fileno())
    os.dup2(null_device, sys.stderr.fileno())
    os.close(null_device)
    # handling signal
    signal.signal(signal.SIGHUP, sig_handle)
    signal.signal(signal.SIGTERM, sig_handle)


def sig_handle(signum, frame):
    '''
    signal handler
    '''
    global LOOP
    # received signal.  Terminate the process gracefully
    LOOP = False
    syslog.syslog('Received signal[{}]'.format(signum))


def delete_pid_file(pid_file):
    syslog.syslog('Removing file[{}]'.format(pid_file))
    os.unlink(pid_file)


def call_file_routing(interval, gatekeeper_jailed_home_base, gatekeeper_home_base, filerouter_jailed_home_dir, gatekeeper_reports_subdir, route_dir, error_dir, archive_dir):
    global LOOP
    try:
        file_routing(gatekeeper_jailed_home_base, gatekeeper_home_base, filerouter_jailed_home_dir, gatekeeper_reports_subdir, route_dir, error_dir, archive_dir)
        if interval > -1:
            time.sleep(interval)
    except OSError as e:
        syslog.syslog('Unexpected error [{}].  Check your configuration.'.format(str(e)))
        LOOP = False
    except Exception as e:
        syslog.syslog('Unexpected exception [{}].  Check your configuration.'.format(str(e)))
        LOOP = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--gatekeeper_jailed_home_base', default='/sftp/opt/edware/home/departures', help='sftp base dir [/sftp/opt/edware/home/departures]')
    parser.add_argument('-g', '--gatekeeper_home_base', default='/opt/edware/home/departures', help='gatekeeper home base dir. [/opt/edware/home/departures]')
    parser.add_argument('-s', '--gatekeeper_report_subdir', default='reports', help='reports directory which saves requesting reports. [reports]')
    parser.add_argument('-f', '--filerouter_jailed_home_dir', default='/sftp/opt/edware/home/filerouter', help='filerouter username. [/sftp/opt/edware/home/filerouter]')
    parser.add_argument('-i', '--interval', default=5, help='Time interval between file checking calls for daemon mode. [5] seconds')
    parser.add_argument('-r', '--route', default='route', help='route directory. [route]')
    parser.add_argument('-e', '--error', default='error', help='error directory. [error]')
    parser.add_argument('-a', '--archive', default='archive', help='archive directory. [archive]')
    parser.add_argument('-b', '--batch', default=False, action='store_true', help='Batch process [False]')
    args = parser.parse_args()
    route_dir = args.route
    error_dir = args.error
    archive_dir = args.archive
    gatekeeper_jailed_home_base = args.gatekeeper_jailed_home_base
    gatekeeper_home_base = args.gatekeeper_home_base
    gatekeeper_reports_subdir = args.gatekeeper_report_subdir
    filerouter_jailed_home_dir = args.filerouter_jailed_home_dir
    interval = args.interval
    batch_process = args.batch

    if batch_process:
        syslog.syslog('Starting filerouter program as batch mode')
        call_file_routing(-1, gatekeeper_jailed_home_base, gatekeeper_home_base, filerouter_jailed_home_dir, gatekeeper_reports_subdir, route_dir, error_dir, archive_dir)
    else:
        daemonize()
        syslog.syslog('Starting filerouter program as daemon mode')
        while LOOP:
            call_file_routing(interval, gatekeeper_jailed_home_base, gatekeeper_home_base, filerouter_jailed_home_dir, gatekeeper_reports_subdir, route_dir, error_dir, archive_dir)
    syslog.syslog('Exiting filerouter program...')
    sys.exit(0)

if __name__ == "__main__":
    main()
