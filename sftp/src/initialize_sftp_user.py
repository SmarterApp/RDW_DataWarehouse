"""
Methods for adding a user that is able to run the UDL

"""
import os
import subprocess
import pwd
import shutil

from src.util import group_exists, create_path


__author__ = 'swimberly'


def create_sftp_user(tenant, user, role, sftp_conf):
    """
    Create an sftp user
    :param tenant: the name of the tenant that the user will belong to
    :param user: the username for the user
    :param role: the role the user will have in the system
    :param sftp_conf: the sftp configuration dictionary
    :return: a tuple containing True if successful, False otherwise and the reason
        as a string
    """
    arrive_depart_dir = sftp_conf['group_directories'][role]
    tenant_path = os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'],
                               arrive_depart_dir, tenant)

    valid_user = _verify_user_tenant_and_role(tenant_path, user, role)
    if not valid_user[0]:
        return False, valid_user[1]

    user_path = os.path.join(tenant_path, user)
    _create_user(user, user_path, role, sftp_conf['file_drop'])
    print('User created:\n\tuser: %s\n\thome dir: %s\n\trole: %s' % (user, user_path, role))
    return True, ""


def delete_user(user):
    """
    Delete the given user from the system and remove thier home folder
    :param user: the user name of the user to delete
    :return: None
    """
    del_user_cmd = "userdel -r {}".format(user)
    subprocess.call(del_user_cmd, shell=True)
    print('user removed:', user)


def _create_user(user, home_folder, role, file_drop_name):
    """
    create the given user with the specified home-folder and group

    :param user: the username of the user to create
    :param home_folder: the path to the users home folder
    :param role: the name of the user's role which will be used to assign a user to a group
    :return: None
    """
    create_path(home_folder)

    add_user_cmd = "adduser -d {} -g {} -s /sbin/nologin {}".format(home_folder, role, user)
    subprocess.call(add_user_cmd, shell=True)
    _create_file_drop_folder(user, home_folder, role, file_drop_name)


def _create_file_drop_folder(user, home_folder, role, file_drop_name):
    """
    Create the directory and set the permissions for the file drop folder
    :param user: the username of the user to create
    :param home_folder: the path to the users home folder
    :param role: the name of the user's role which will be used to assign a user to a group
    :param file_drop_name: the name of the file drop folder (should be in the sftp_config dict)
    :return: None
    """
    file_drop_loc = os.path.join(home_folder, file_drop_name)
    # create file drop location and set proper permission
    create_path(file_drop_loc)
    shutil.chown(file_drop_loc, user, role)
    os.chmod(file_drop_loc, 0o777)


def _verify_user_tenant_and_role(tenant_path, username, role):
    """
    Verify that the username does not already exist and that the tenant does exist

    :param tenant_path: The path to the tenant directory
    :param username: The name of the user being created
    :param role: The role of the user being created (group)
    :return: True if both the tenant and the user are valid, False otherwise
    """
    # Ensure that tenant has already been created
    if not os.path.exists(tenant_path):
        return False, 'Tenant does not exist!'

    # check that the role has been created as a group on the system
    if not group_exists(role):
        return False, 'Role does not exist as a group in the system'

    # Verify that user does not already exist
    try:
        pwd.getpwnam(username)
        return False, 'User already exists!'
    except KeyError:
        return True, ""


def _set_ssh_key(home_folder, pub_key_str=None, pub_key_file=None):
    """
    Add the given public key to the users home folder
    :param home_folder:
    :param pub_key_str: The string containing the public key
    :param pub_key_file: The file containing the public key
    :return: None
    """
    pass
