'''
Authoritative Definitions for UDL's required tables

UDL_METADATA contains all tables, sequences that are used in UDL system

Several methods are provided to create/drop tables/sequences/extensions/foreign data wrapper servers
in postgres database.

Main Method: setup_udl2_schema(conf)
Main method: teardown_udl2_schema(conf)

conf is defined in udl2_conf.py, default is under /opt/wgen/edware-udl/etc/udl2_conf.py

Created on May 10, 2013

@author: ejen
'''
from sqlalchemy.schema import (MetaData, CreateSchema, CreateSequence, ForeignKeyConstraint, UniqueConstraint)
from sqlalchemy import Table, Column, Sequence
from sqlalchemy.types import *
from sqlalchemy.sql.expression import text
import argparse
from config import ref_table_data, sr_ref_table_data
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2_util.database_util import connect_db, execute_queries
from edudl2.udl2.populate_ref_info import populate_ref_column_map, populate_stored_proc
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.metadata.udl2_metadata import generate_udl2_metadata, generate_udl2_sequences


def _parse_args():
    '''
    private method to parse command line options when call from shell. We use it to setup/teardown database
    automatically by configuration (this helps jenkins/Continous Integration)
    '''
    parser = argparse.ArgumentParser('database')
    parser.add_argument('--config_file', dest='config_file',
                        help="full path to configuration file for UDL2, default is /opt/wgen/edware-udl/etc/udl2_conf.py")
    parser.add_argument('--action', dest='action', required=False,
                        help="'setup' for setting up udl2 database. " +
                             "'teardown' for tear down udl2 database")
    args = parser.parse_args()
    return (parser, args)


def _create_conn_engine(udl2_conf):
    '''
    private method to create database connections via database_util
    @param udl2_conf: The configuration dictionary for databases
    '''
    (conn, engine) = connect_db(udl2_conf['db_driver'],
                                udl2_conf['db_user'],
                                udl2_conf['db_pass'],
                                udl2_conf['db_host'],
                                udl2_conf['db_port'],
                                udl2_conf['db_name'])
    return (conn, engine)


def map_sql_type_to_sqlalchemy_type(sql_type):
    '''
    map sql data type in configuration file into what SQLAlchemy type is.
    @param sql_type: sql data type
    '''
    mapped_type = None
    sql_type_mapped_type = {
        'timestamp': TIMESTAMP,
        'timestamp with time zone': TIMESTAMP(True),
        'bigint': BIGINT,
        'smallint': SMALLINT,
        'bigserial': BIGINT,
        'varchar': VARCHAR,
        'double': FLOAT,
        'json': TEXT,
        'text': TEXT,
        'bool': BOOLEAN,
        'interval': Interval,
        'time': Time
    }
    try:
        mapped_type = sql_type_mapped_type[sql_type]
    except Exception as e:
        if sql_type[0:7] == 'varchar':
            length = int(sql_type[7:].replace('(', '').replace(')', ''))
            mapped_type = VARCHAR(length)
    return mapped_type


def map_tuple_to_sqlalchemy_column(ddl_tuple):
    '''
    create a SQLAlchemy Column object from UDL_METADATA column
    @param ddl_tuple: column definition in UDL_METADATA
    '''
    column = Column(ddl_tuple[0],
                    map_sql_type_to_sqlalchemy_type(ddl_tuple[2]),
                    primary_key=ddl_tuple[1],
                    nullable=ddl_tuple[4],
                    server_default=(text(ddl_tuple[3]) if (ddl_tuple[3] != '') else None),
                    doc=ddl_tuple[5],)
    # print(column)
    return column


def create_table_keys(key_ddl_dict, schema):
    '''
    Take a dictionary of key lists. Will check for 'foreign' and 'unique' in the list
    and create sqlalchemy ForeignKeys objects and UniqueKey objects, respectively
    @param key_ddl_dict: A dictionary containing key information. Each value should be a list of tuples.
    the unique key tuple will contain any number of columns that constitute the unique combination. ('col1', 'col2', ...)
    the foreign key tuple will contain the column in the current table and
    the table and column in the other table. ie: ('col1', 'table2.col2')
    @type key_ddl_dict: dict
    @return: A list of foreign and unique keys
    @rtype: list
    '''
    key_list = []
    unique_keys = key_ddl_dict.get('unique', [])
    foreign_keys = key_ddl_dict.get('foreign', [])

    for uk_tup in unique_keys:
        ukc = UniqueConstraint(*uk_tup)
        key_list.append(ukc)

    for fk_tup in foreign_keys:
        foreign_column = schema + '.' + fk_tup[1]
        fk_name = "%s-%s" % (fk_tup[0], foreign_column)
        fkc = ForeignKeyConstraint([fk_tup[0]], [foreign_column], name=fk_name, use_alter=True)
        key_list.append(fkc)

    return key_list


def create_table(metadata, table_name):
    '''
    create a table from UDL_METADATA definitions
    @param udl2_conf: The configuration dictionary for udl
    @param metadata: SQLAlchemy Metadata object
    @param scheam: Schema name where the table is located in UDL2 schema
    @param table_name: Table name for the table to be created, it must be defined in UDL_METADATA
    '''
    #print('create table metadata %s' % table_name)
    column_ddl = UDL_METADATA['TABLES'][table_name]['columns']
    key_ddl = UDL_METADATA['TABLES'][table_name]['keys']
    arguments = [table_name, metadata]

    for c_ddl in column_ddl:
        #print(c_ddl)
        column = map_tuple_to_sqlalchemy_column(c_ddl)
        arguments.append(column)

    # create unique and foreign table keys, Add to arguments
    # arguments += create_table_keys(key_ddl, schema)
    table = Table(*tuple(arguments))

    return table


def drop_table(udl2_conf, schema, table_name):
    '''
    drop a table
    @param udl2_conf: The configuration dictionary for
    @param scheam: Schema name where the table is located in UDL2 schema
    @param table_name: Table name for the table to be created, it must be defined in UDL_METADATA
    '''
    print('drop table %s.%s' % (schema, table_name))
    sql = text("DROP TABLE IF EXISTS \"%s\".\"%s\" CASCADE" % (schema, table_name))
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop table %s.%s" % (schema, table_name)
    execute_queries(conn, [sql], except_msg)


def create_sequence(connection, metadata, schema, seq_name):
    '''
    create a sequence from UDL_METADATA definitions
    @param udl2_conf: The configuration dictionary for udl
    @param metadata: SQLAlchemy Metadata object
    @param schema: Schema name where the table is located in UDL2 schema
    @param seq_name: sequence name for the sequence to be created, it must be defined in UDL_METADATA
    '''
    print('create global sequence')
    sequence_ddl = UDL_METADATA['SEQUENCES'][seq_name]
    sequence = Sequence(name=sequence_ddl[0],
                        start=sequence_ddl[1],
                        increment=sequence_ddl[2],
                        schema=schema,
                        optional=sequence_ddl[3],
                        quote=sequence_ddl[4],
                        metadata=metadata)
    connection.execute(CreateSequence(sequence))

    #except_msg = "fail to create sequence %s.%s" % (schema, seq_name)
    #execute_queries(conn, [sql], except_msg)
    return sequence


def drop_sequence(udl2_conf, schema, seq_name):
    '''
    drop schemas according to configuration file
    @param udl2_conf: The configuration dictionary for udl
    @param schema: Schema name where the table is located in UDL2 schema
    @param seq_name: sequence name for the sequence to be created, it must be defined in UDL_METADATA
    '''
    print('drop global sequences')
    sql = text("DROP SEQUENCE \"%s\".\"%s\" CASCADE" % (schema, seq_name))
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop sequence %s.%s" % (schema, seq_name)
    execute_queries(conn, [sql], except_msg)


#def create_udl2_schema(udl2_conf):
#    '''
#    create schemas according to configuration file
#    @param udl2_conf: The configuration dictionary for
#    '''
#    print('create udl2 staging schema')
#    sql = text("CREATE SCHEMA \"%s\"" % udl2_conf['staging_schema'])
#    (conn, engine) = _create_conn_engine(udl2_conf)
#    except_msg = "fail to create schema %s" % udl2_conf['staging_schema']
#    execute_queries(conn, [sql], except_msg)


def drop_udl2_schema(udl2_conf):
    '''
    drop schemas according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop udl2 staging schema')
    sql = text("DROP SCHEMA \"%s\" CASCADE" % udl2_conf['staging_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop udl2 schema %s" % udl2_conf['staging_schema']
    execute_queries(conn, [sql], except_msg)


def create_udl2_tables(udl2_conf):
    '''
    create tables in schema according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    # engine = (_get_db_url(udl2_conf))
    udl2_metadata = generate_udl2_metadata(udl2_conf['staging_schema'])
    print("create tables")

    (conn, engine) = _create_conn_engine(udl2_conf)

    # Use metadata to create tables
    udl2_metadata.create_all(engine)


def drop_udl2_tables(udl2_conf):
    '''
    drop tables according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print("drop tables")
    for table, definition in UDL_METADATA['TABLES'].items():
        drop_table(udl2_conf, udl2_conf['staging_schema'], table)


def create_udl2_sequence(connection, schema_name, udl2_metadata):
    '''
    create sequences according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    # (conn, engine) = _create_conn_engine(udl2_conf['udl2_db'])
    #udl2_metadata = MetaData()
    print("create sequences")
    for sequence in generate_udl2_sequences(schema_name, udl2_metadata):
        connection.execute(CreateSequence(sequence))


def drop_udl2_sequences(udl2_conf):
    '''
    drop sequences according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print("drop sequences")
    for seq, definition in UDL_METADATA['SEQUENCES'].items():
        drop_sequence(udl2_conf, udl2_conf['staging_schema'], seq)


def create_foreign_data_wrapper_extension(udl2_conf):
    '''
    create foreign data wrapper extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('create foreign data wrapper extension')
    sql = "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA %s" % (udl2_conf['csv_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create foreign data wrapper extension"
    execute_queries(conn, [sql], except_msg)


def drop_foreign_data_wrapper_extension(udl2_conf):
    '''
    drop foreign data wrapper extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop foreign data wrapper extension')
    sql = "DROP EXTENSION IF EXISTS file_fdw CASCADE"
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop foreign data wrapper extension"
    execute_queries(conn, [sql], except_msg)


def create_dblink_extension(udl2_conf):
    '''
    create dblink extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('create dblink extension')
    sql = "CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA %s" % (udl2_conf['db_schema'])
    print(sql)
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create dblink extension"
    execute_queries(conn, [sql], except_msg)


def drop_dblink_extension(udl2_conf):
    '''
    drop dblink extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop dblink extension')
    sql = "DROP EXTENSION IF EXISTS dblink CASCADE"
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop dblink extension"
    execute_queries(conn, [sql], except_msg)


def create_foreign_data_wrapper_server(udl2_conf):
    '''
    create server for foreign data wrapper according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('create foreign data wrapper server')
    sql = "CREATE SERVER %s FOREIGN DATA WRAPPER file_fdw" % (udl2_conf['fdw_server'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create foreign data wrapper server"
    execute_queries(conn, [sql], except_msg)


def drop_foreign_data_wrapper_server(udl2_conf):
    '''
    drop server for foreign data wrapper according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop foreign data wrapper server')
    sql = "DROP SERVER IF EXISTS %s CASCADE" % (udl2_conf['fdw_server'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop foreign data wrapper server"
    execute_queries(conn, [sql], except_msg)


def load_fake_record_in_star_schema(udl2_conf):
    '''
    load two fake records into dim_int_hier and dim_section for integration table to create
    star schema from integration table
    @param udl2_conf: The configuration dictionary for
    '''
    print('load fake record')
    (conn, engine) = _create_conn_engine(udl2_conf)
    sqls = [
        """
        INSERT INTO "{schema_name}"."dim_section"(
            section_rec_id, section_guid, section_name, grade, class_name,
            subject_name, state_code, district_guid, school_guid, from_date,
            to_date, most_recent)
        VALUES (1, 'fake_value', 'fake_value', 'fake_value', 'fake_value',
            'fake_value', 'FA', 'fake_value', 'fake_value', '99999999',
            '00000000', False);
        """.format(schema_name=udl2_conf['db_schema']),
        """
        INSERT INTO "{schema_name}"."dim_inst_hier"(
            inst_hier_rec_id, state_name, state_code, district_guid, district_name,
            school_guid, school_name, school_category, from_date, to_date,
            most_recent)
        VALUES (-1, 'fake_value', 'FA', 'fake_value', 'fake_value',
            'fake_value', 'fake_value', 'fake_value', '99999999', '00000000',
            False);
        """.format(schema_name=udl2_conf['db_schema']),
    ]
    except_msg = "fail to drop foreign data wrapper server"
    execute_queries(conn, sqls, except_msg)


def load_reference_data(udl2_conf):
    '''
    load the reference data into the reference tables
    @param udl2_conf: The configuration dictionary for
    '''
    (conn, engine) = _create_conn_engine(udl2_conf)
    asmt_ref_table_info = ref_table_data.ref_table_conf
    populate_ref_column_map(asmt_ref_table_info, engine, conn, udl2_conf['reference_schema'], udl2_conf['ref_tables']['assessment'])

    sr_ref_table_info = sr_ref_table_data.ref_table_conf
    populate_ref_column_map(sr_ref_table_info, engine, conn, udl2_conf['reference_schema'], udl2_conf['ref_tables']['studentregistration'])


def load_stored_proc(udl2_conf):
    '''
    Generate and load the stored procedures to be used for transformations and
    validations into the database.
    @param udl2_conf: The configuration dictionary for
    '''

    (conn, engine) = _create_conn_engine(udl2_conf)
    populate_stored_proc(engine, conn, udl2_conf['reference_schema'], udl2_conf['ref_tables']['assessment'],
                         udl2_conf['ref_tables']['studentregistration'])


###
# NEW METHODS TO MAKE METADATA USAGE SIMPLER
###

def create_udl2_schema(engine, connection, schema_name, bind=None):
    """

    :param engine:
    :param connection:
    :param schema_name:
    :param bind:
    :return:
    """
    metadata = generate_udl2_metadata(schema_name, bind=bind)
    connection.execute(CreateSchema(metadata.schema))
    metadata.create_all(bind=engine)
    return metadata


####
## END NEW METHODS
####

def setup_udl2_schema(udl2_conf):
    '''
    create whole udl2 database schema according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    # Create schema, tables and sequences
    (udl2_db_conn, udl2_db_engine) = _create_conn_engine(udl2_conf['udl2_db'])
    udl2_schema_name = udl2_conf['udl2_db']['db_schema']
    udl2_metadata = create_udl2_schema(udl2_db_engine, udl2_db_conn, udl2_schema_name)
    create_udl2_sequence(udl2_db_conn, udl2_schema_name, udl2_metadata)

    # create db_link and fdw
    create_dblink_extension(udl2_conf['target_db'])
    create_dblink_extension(udl2_conf['udl2_db'])
    create_foreign_data_wrapper_extension(udl2_conf['udl2_db'])
    create_foreign_data_wrapper_server(udl2_conf['udl2_db'])

    # load data and stored procedures
    load_fake_record_in_star_schema(udl2_conf['target_db'])
    load_reference_data(udl2_conf['udl2_db'])
    load_stored_proc(udl2_conf['udl2_db'])


def teardown_udl2_schema(udl2_conf):
    '''
    drop whole udl2 database schema according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    drop_udl2_sequences(udl2_conf['udl2_db'])
    drop_udl2_tables(udl2_conf['udl2_db'])
    drop_foreign_data_wrapper_server(udl2_conf['udl2_db'])
    drop_foreign_data_wrapper_extension(udl2_conf['udl2_db'])
    drop_dblink_extension(udl2_conf['udl2_db'])
    drop_udl2_schema(udl2_conf['udl2_db'])
    drop_dblink_extension(udl2_conf['target_db'])


def main():
    '''
    create or drop udl2 database objects according to command line.
    The purpose for this script is to enable clean up whole database artifacts or create
    whole database artifacts without problem. Since UDL uses databases to clean data. Database object
    in UDL can be dropped or recreated at will for changes. So we can verifiy system
    '''
    (parser, args) = _parse_args()
    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file
    conf_tup = read_ini_file(config_path_file)
    udl2_conf = conf_tup[0]

    if args.action is None:
        parser.print_help()
    if args.action == 'setup':
        setup_udl2_schema(udl2_conf)
    elif args.action == 'teardown':
        teardown_udl2_schema(udl2_conf)

if __name__ == '__main__':
    main()
