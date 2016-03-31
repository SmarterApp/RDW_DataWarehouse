# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Oct 20, 2015

@author: tosako
'''
from edcore.database import initialize_db
from edmigrate.migrate.migrate_helper import yield_rows
import configparser
from sqlalchemy.sql.expression import select
import random
import string
import hmac
from hashlib import sha1
import argparse
from edmigrate.database.migrate_public_connector import EdMigratePublicConnection
from edmigrate.database.migrate_private_connector import EdMigratePrivateConnection
from edmigrate.utils.utils import create_daemon
from edcore.utils.utils import run_cron_job
import time
from public_report.recache import trigger_public_report_precache
from smarter.trigger.pre_cache_generator import read_config_from_json_file
from pyramid_beaker import set_cache_regions_from_settings
from sqlalchemy.schema import DropSchema, CreateSchema
from edcore.database.routing import PublicDBConnection

TABLE_LIST = ['dim_inst_hier', 'dim_student', 'dim_asmt', 'custom_metadata', 'fact_asmt_outcome_vw', 'fact_block_asmt_outcome', 'fact_asmt_outcome']
PII_FIELD = {'external_student_id', 'first_name', 'middle_name', 'last_name', 'birthdate', 'where_taken_id', 'where_taken_name'}
MASK_FIELD = {'student_id', 'district_id', 'school_id', 'asmt_guid'}
SHUFFLE_ID = {'student_rec_id', 'inst_hier_rec_id', 'asmt_rec_id', 'asmt_outcome_vw_rec_id', 'asmt_outcome_rec_id'}
lookup_dict = {}

public_tenant = None
private_tenant = None
no_recache = False
cache_only = False
PID_FILE = '/opt/edware/run/edmigrate_public.{}.pid'


def _setup_db_connection(settings):
    '''
    Initialize database connection
    '''
    initialize_db(EdMigratePublicConnection, settings)
    initialize_db(EdMigratePrivateConnection, settings)
    initialize_db(PublicDBConnection, settings)


def _delete_data(public_tenant):
    '''
    delete all data from tables.
    '''
    with EdMigratePublicConnection(public_tenant) as public_conn:
        metadata = public_conn.get_metadata()
        try:
            public_conn.execute(DropSchema(metadata.schema, cascade=True))
            public_conn.execute(CreateSchema(metadata.schema))
            #metadata = generate_ed_metadata(schema_name=public_tenant, bind=engine)
            public_conn.execute('CREATE SEQUENCE "' + metadata.schema + '"."global_rec_seq"')
            metadata.create_all(public_conn.get_engine())
        except:
            for table_name in reversed(TABLE_LIST):
                public_table = public_conn.get_table(table_name)
                public_conn.execute(public_table.delete())


def _generate_passphrase(size):
    '''
    creating disposable passphrase
    size must be 16, 24, 32; otherwise, AES ecnryption will fail (will throw an exception)
    '''
    return ''.join(random.choice(string.printable) for _ in range(size))


def _get_dict(name_of_dict):
    requested_dict = None
    if name_of_dict not in lookup_dict:
        requested_dict = {}
        lookup_dict[name_of_dict] = requested_dict
    else:
        requested_dict = lookup_dict[name_of_dict]
    return requested_dict


def _randomize_id(fields):
    '''
    assign new id for existing id.
    '''
    for shuffle_id in SHUFFLE_ID:
        if shuffle_id in fields:
            # we use 2 dict to make sure we do not have id collisions.
            id_lookup = _get_dict(shuffle_id + '_lookup')
            id_reverse_lookup = _get_dict(shuffle_id + '_reverse_lookup')
            while fields[shuffle_id] not in id_lookup:
                # 9223372036854775807 is maximum bigint for postgresql 2^63-1
                new_id = random.randint(0, 9223372036854775807)
                if new_id not in id_reverse_lookup:
                    id_reverse_lookup[new_id] = fields[shuffle_id]
                    id_lookup[fields[shuffle_id]] = new_id
            fields[shuffle_id] = id_lookup[fields[shuffle_id]]


def _mask_id(fields, key):
    '''
    masking id
    we mask id because we cannot remove id because of postgresql constraint and not because of report needs.
    1. apply aes encryption.
    2. apply sha1 hash to limit string 40 bytes (or 160 bits)
    '''
    for mask in MASK_FIELD:
        if mask in fields and (fields[mask] is not None or not fields[mask]):
            # need to mask data, use sha1 hash to keep hash data within 40 bytes string
            hashed = hmac.new(key, fields[mask].encode(), sha1)
            fields[mask] = hashed.hexdigest()


def _clear_batch_guid(fields):
    '''
    just need to remove batch_guid because it is useless information for public
    also prevent backtracking
    '''
    if 'batch_guid' in fields:
        fields['batch_guid'] = ''


def _create_query_without_pii(table):
    '''
    create sql select query from given table object without PII fields.
    '''
    # Create Select statement without PII fields
    select_query = select([column for column in table.c._all_columns if column.name not in PII_FIELD])
    # Need only rec_status is 'C'urrent
    if 'rec_status' in table.c:
        return select_query.where(table.c['rec_status'] == 'C')
    return select_query


def process_row(row, key):
    '''
    apply randomize id, mask id, and clear batch guid process to given row
    '''
    fields = dict(row.items())
    _randomize_id(fields)
    _mask_id(fields, key)
    _clear_batch_guid(fields)
    return fields


def copy_data_without_PII(private_tenant, public_tenant, fetch_size=500):
    '''
    copy data from private tenant to public tenant without PII
    '''
    # Create AES instance for masking data
    # generate disposable passphrase, so that nobody can decrypt.
    key = _generate_passphrase(32).encode()
    with EdMigratePublicConnection(public_tenant) as public_db_conn:
        with EdMigratePrivateConnection(private_tenant) as private_db_conn:
            for table_name in TABLE_LIST:
                private_table = private_db_conn.get_table(table_name)
                public_table = public_db_conn.get_table(table_name)
                select_query = _create_query_without_pii(private_table)
                # Retrive data fetch_size at a time
                proxy_rows = yield_rows(private_db_conn, select_query, fetch_size)
                for rows in proxy_rows:
                    value_list = []
                    for row in rows:
                        value_list.append(process_row(row, key))
                    public_db_conn.execute(public_table.insert().values(value_list))


def main():
    parser = argparse.ArgumentParser(description='Transform private data to public data')
    parser.add_argument('-i', dest='ini', help="The path to the ini file",
                        default="/opt/edware/conf/smarter.ini")
    parser.add_argument('-t', dest='tenant', help="target tenant", required=True)
    parser.add_argument('-d', dest='daemon', action='store_true', default=False, help="daemon mode")
    parser.add_argument('-p', dest='pidfile', help="pid file for daemon")
    parser.add_argument('-c', dest='cache_only', action='store_true', default=False, help="recache only, only works without -d option")
    parser.add_argument('-n', dest='no_recache', action='store_true', default=False, help="do not recache")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.ini)
    global private_tenant
    private_tenant = args.tenant
    global public_tenant
    public_tenant = args.tenant
    global no_recache
    no_recache = args.no_recache
    daemon = args.daemon
    pid_file = (args.pidfile if args.pidfile is not None else PID_FILE).format(args.tenant)
    if daemon:
        create_daemon(pid_file)
        run_cron_job(config['app:main'], 'migrate_public.', process)
        while True:
            time.sleep(1000)
    else:
        global cache_only
        cache_only = args.cache_only
        process(config['app:main'])


def process(settings):
    _setup_db_connection(settings)
    if not cache_only:
        _delete_data(public_tenant)
        copy_data_without_PII(private_tenant, public_tenant)
    if not no_recache:
        filter_settings = read_config_from_json_file(settings.get('migrate_public.recache.filter.file'))
        set_cache_regions_from_settings(settings)
        trigger_public_report_precache(public_tenant, filter_settings)


if __name__ == '__main__':
    main()
