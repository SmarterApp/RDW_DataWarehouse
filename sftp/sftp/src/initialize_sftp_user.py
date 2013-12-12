"""
Methods for adding a user that is able to run the UDL

"""
import os
import subprocess
import pwd
import shutil
from sftp.src.util import cleanup_directory, create_path, group_exists,\
    change_owner


__author__ = 'swimberly'


def get_user_home_dir(sftp_conf, tenant, user, role):
    '''
    Returns the users's home directory
    '''
    arrive_depart_dir = sftp_conf['sftp_arrivals_dir'] if role is 'sftparrivals' else sftp_conf['sftp_departures_dir']
    return os.path.join(sftp_conf['user_home_base_dir'], arrive_depart_dir, tenant, user)


def get_user_sftp_jail_dir(sftp_conf, tenant, user, role):
    '''
    Returns user's jail directory
    '''
    tenant_path = get_tenant_sftp_jail_dir(sftp_conf, tenant, role)
    return os.path.join(tenant_path, user)


def get_tenant_sftp_jail_dir(sftp_conf, tenant, role):
    if role == 'sftparrivals':
        arrive_depart_dir = sftp_conf['sftp_arrivals_dir']
    elif role == 'sftpdepartures':
        arrive_depart_dir = sftp_conf['sftp_departures_dir']
    else:
        arrive_depart_dir = sftp_conf['sftp_filerouter_dir']
        tenant = ""
    return os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'], arrive_depart_dir, tenant)


def get_user_path(sftp_conf, role):
    if role == 'sftparrivals':
        user_path = sftp_conf['user_path_sftparrivals_dir']
    elif role == 'sftpdepartures':
        user_path = sftp_conf['user_path_sftpdepartures_dir']
    else:
        user_path = sftp_conf['user_path_filerouter_dir']
    return user_path


def create_sftp_user(tenant, user, role, sftp_conf, ssh_key_str=None, ssh_key_file=None):
    """
    Create an sftp user
    :param tenant: the name of the tenant that the user will belong to
    :param user: the username for the user
    :param role: the role the user will have in the system
    :param sftp_conf: the sftp configuration dictionary
    :return: a tuple containing True if successful, False otherwise and the reason
        as a string
    """
    tenant_sftp_path = get_tenant_sftp_jail_dir(sftp_conf, tenant, role)
    valid_user = _verify_user_tenant_and_role(tenant_sftp_path, user, role)
    if not valid_user[0]:
        print("Error: {}".format(valid_user[1]))
        return False, valid_user[1]

    user_sftp_path = get_user_sftp_jail_dir(sftp_conf, tenant, user, role)
    user_home_path = get_user_home_dir(sftp_conf, tenant, user, role)
    user_path = get_user_path(sftp_conf, role)

    _create_user(user, user_home_path, user_sftp_path, sftp_conf['group'], user_path)

    # set ssh keys if provided
    if ssh_key_file or ssh_key_str:
        _set_ssh_key(user, role, user_home_path, ssh_key_str, ssh_key_file)

    print('User created:\n\tuser: {}\n\thome dir: {}\n\tsftp dir: {}\n\trole: {}'.format(user, user_home_path,
                                                                                         user_sftp_path, role))
    return True, ""


def delete_user(user, sftp_conf):
    """
    Delete the given user from the system and remove thier home folder
    :param user: the user name of the user to delete
    :return: None
    """

    # if the user does not exist return immediately
    if _check_user_not_exists(user)[0]:
        return

    tenant_name = os.path.split(os.path.dirname(pwd.getpwnam(user).pw_dir))[-1]

    subprocess.call(['userdel', '-r', user])

    # check both arrivals and departures in the sftp directores to delete user
    sftp_path_1 = os.path.join(get_user_sftp_jail_dir(sftp_conf, tenant_name, user, 'sftparrivals'))
    sftp_path_2 = os.path.join(get_user_sftp_jail_dir(sftp_conf, tenant_name, user, 'sftpdepartures'))
    cleanup_directory(sftp_path_1)
    cleanup_directory(sftp_path_2)

    print('user removed:', user)


def _create_user(user, home_folder, sftp_folder, role, directory_name):
    """
    create the given user with the specified home-folder and group

    :param user: the username of the user to create
    :param home_folder: the path to the users home folder
    :param role: the name of the user's role which will be used to assign a user to a group
    :return: None
    """
    create_path(sftp_folder)

    subprocess.call(['adduser', '-d', home_folder, '-g', role, '-s', '/sbin/nologin', user])
    _create_role_specific_folder(user, sftp_folder, role, directory_name)


def _create_role_specific_folder(user, sftp_user_folder, role, directory_name):
    """
    Create the directory and set the permissions for the file drop folder
    :param user: the username of the user to create
    :param sftp_user_folder: the path to the users home folder
    :param role: the name of the user's role which will be used to assign a user to a group
    :param file_drop_name: the name of the file drop folder (should be in the sftp_config dict)
    :return: None
    """
    file_drop_loc = os.path.join(sftp_user_folder, directory_name)
    # Change the user's home sftp to a+rw
    os.chmod(sftp_user_folder, 0o705)

    # create file drop location and set proper permission
    create_path(file_drop_loc)
    change_owner(file_drop_loc, user, role)


def _verify_user_tenant_and_role(tenant_path, username, role):
    """
    Verify that the username does not already exist and that the tenant does exist

    :param tenant_path: The path to the tenant directory
    :param username: The name of the user being created
    :param role: The role of the user being created (group)
    :return: True if both the tenant and the user are valid, False otherwise
    """
    # Ensure that tenant has already been created
    if role != 'filerouter' and not os.path.exists(tenant_path):
        return False, 'Tenant does not exist!'

    # check that the role has been created as a group on the system
    if not group_exists(role):
        return False, 'Role does not exist as a group in the system'

    # Verify that user does not already exist
    return _check_user_not_exists(username)


def _check_user_not_exists(username):
    """
    Check that a user does not _check_user_not_exists
    If the user exists return false and a string.
    If the user does not exist true and an empty string are returned
    """
    try:
        pwd.getpwnam(username)
        return False, 'User already exists!'
    except KeyError:
        return True, ""


def _set_ssh_key(user, role, home_folder, pub_key_str=None, pub_key_file=None):
    """
    Add the given public key to the users home folder
    :param home_folder:
    :param pub_key_str: The string containing the public key
    :param pub_key_file: The file containing the public key
    :return: None
    """
    if not pub_key_str and not pub_key_file:
        return

    ssh_dir = os.path.join(home_folder, '.ssh')
    create_path(ssh_dir)

    auth_keys_path = os.path.join(home_folder, '.ssh', 'authorized_keys')

    pub_key = pub_key_str
    if not pub_key_str:
        with open(pub_key_file, 'r') as f:
            pub_key = f.read()
    with open(auth_keys_path, 'a') as f:
        f.write(pub_key)
        if pub_key[-1] != '\n':
            f.write('\n')

    shutil.chown(ssh_dir, user, role)
    shutil.chown(auth_keys_path, user, role)
