__author__ = 'sravi'

import imp
import argparse
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.database_util import connect_db, execute_queries


def _create_conn_engine(udl2_conf):
    """
    private method to create database connections via database_util
    @param udl2_conf: The configuration dictionary for databases
    """
    (conn, engine) = connect_db(udl2_conf['db_driver'],
                                udl2_conf['db_user'],
                                udl2_conf['db_pass'],
                                udl2_conf['db_host'],
                                udl2_conf['db_port'],
                                udl2_conf['db_name'])
    return (conn, engine)


def create_tenant_master_metadata(udl2_conf):
    (conn, engine) = _create_conn_engine(udl2_conf)
    pass


def remove_tenant_master_metadata(udl2_conf):
    (conn, engine) = _create_conn_engine(udl2_conf)
    pass


def _parse_args():
    """
    private method to parse command line options when call from shell
    """
    parser = argparse.ArgumentParser(description='Process tenant management args')
    parser.add_argument('--config_file', dest='config_file', help="full path to configuration file for UDL2, default is /opt/wgen/edware-udl/etc/udl2_conf.py")
    parser.add_argument('--action', dest='action', required=True, help="'add' for adding a new tenant to star schema. 'remove' for removing a tenant from star schema")
    parser.add_argument('--tenant', dest='tenant', required=True, help="tenant name to be added or removed")

    args = parser.parse_args()
    return (parser, args)


def main():
    """
    utility script to support tenant management
    """
    (parser, args) = _parse_args()
    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file
    udl2_conf = imp.load_source('udl2_conf', config_path_file)
    from udl2_conf import udl2_conf

    if args.action is None:
        parser.print_help()
    if args.action == 'add':
        create_tenant_master_metadata(udl2_conf['udl2_db'])
    elif args.action == 'remove':
        remove_tenant_master_metadata(udl2_conf['udl2_db'])

if __name__ == '__main__':
    main()
