'''
Populate data in pre_prod database for testing purposes
Created on Mar 11, 2014

@author: dip
'''
import os
from edudl2.database.udl2_connector import initialize_db_prod, PRODUCTION_NAMESPACE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edschema.database.data_importer import import_csv_dir


def main():
    try:
        config_path_file = os.environ['UDL2_CONF']
    except Exception:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    udl2_conf, udl2_flat_conf = read_ini_file(config_path_file)
    initialize_db_prod(udl2_conf)
    load_data('ca')


def load_data(tenant_name):
    '''
    Load sds data into prod database
    '''
    here = os.path.abspath(os.path.dirname(__file__))
    resource_dir = os.path.join(here, '../../edschema/edschema/database/tests/resources/')
    import_csv_dir(resource_dir, PRODUCTION_NAMESPACE + "." + tenant_name)


if __name__ == "__main__":
    main()
