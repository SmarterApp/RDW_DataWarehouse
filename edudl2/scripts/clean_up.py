'''
Clean up temporary schemas
'''
import os
import re
from edudl2.database.udl2_connector import initialize_db_target, get_target_connection
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE


def main():
    config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    udl2_conf, udl2_flat_conf = read_ini_file(config_path_file)
    initialize_db_target(udl2_conf)
    clean_up_unused_schemas()

def clean_up_unused_schemas():
    with get_target_connection() as conn:
        schemas = conn.execute("select schema_name from information_schema.schemata")
        for schema in schemas:
            schema_name = schema[0]
            if re.match('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', schema_name):
                drop_schema_by_name(conn, schema_name)


def drop_schema_by_name(conn, schema_name):
    conn.execute('drop schema "%s" cascade' % schema_name)


if __name__ == "__main__":
    main()
