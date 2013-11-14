'''
Created on Nov 11, 2013

@author: tosako
'''
import os
import stat
import shutil
import syslog

def _route_file(from_file, to_file, file_owner=None):
    '''
    copy file from_file to to_file
    '''
    if '/error/' in to_file:
        # if to_file is error, just move the file.
        if os.path.isfile(to_file):
            os.unlink(to_file)
        to_file_dir = os.path.dirname(to_file)
        if not os.path.isdir(to_file_dir):
            os.makedirs(to_file_dir, mode=0o700, exist_ok=True)
        os.rename(from_file, to_file)
        syslog.syslog(syslog.LOG_INFO, 'File moved: [{}] to [{}]'.format(from_file, to_file))
    else:
        # rename file to indicate that file is being copying.
        working_file = from_file + '.process'
        filedir, filename = os.path.split(to_file)
        hidden_to_file=os.path.join(filedir, "." + filename)
        os.rename(from_file, working_file)
        try:
            shutil.copyfile(working_file, hidden_to_file)
        except:
            #failed at copy. revert filename and route file to error.
            syslog.syslog(syslog.LOG_ERR, 'Failed copy file: [{}] to [{}]'.format(from_file, to_file))
            os.rename(working_file, from_file)
            _route_file(from_file, _get_error_filename(from_file))
        os.chmod(hidden_to_file, mode=0o700)
        if file_owner is not None:
            os.chown(hidden_to_file, file_owner, -1)
        os.rename(hidden_to_file, to_file)
        os.unlink(working_file)
        syslog.syslog(syslog.LOG_INFO, 'File moved: [{}] to [{}]'.format(from_file, to_file))
        
    

def _find_files(base, suffix='.zip'):
    '''
    find "*.zip" file recursively by given base dir.
    '''
    filenames = []
    if base is not None:
        mode = os.stat(base).st_mode
        if stat.S_ISREG(mode):
            if os.path.basename(base).endswith(suffix):
                filenames.append(base)
        elif stat.S_ISDIR(mode):
            dirs = os.listdir(base)
            for file in dirs:
                filenames += _find_files(os.path.join(base, file))
    return filenames


def _get_destination_filename_for_gatekeeper(jailed_home_base, original_file_name):
    '''
    copy file from router account to gatekeeper jailed account
    '''
    path = original_file_name.split(os.path.sep)
    filename = path.pop()
    gatekeeper = path.pop()
    tenant = path.pop()
    #check if jailed account path exist.
    gatekeeper_home_dir = os.path.join(jailed_home_base, tenant, gatekeeper)
    if os.path.isdir(gatekeeper_home_dir):
        # check the file has existed already.
        destination_filename = os.path.join(gatekeeper_home_dir, filename)
        if os.path.isfile(destination_filename):
            # file should not be existed there.
            # failed condition
            destination_filename = _get_error_filename(original_file_name)
    else:
        # most likely sftp jailed account has not created.
        # failed condition
        destination_filename = _get_error_filename(original_file_name)
    return destination_filename

def _get_error_filename(original_file_name):
    return original_file_name.replace("/route/", "/error/")

def main():
    pass

if __name__ == "__main__":
    main()