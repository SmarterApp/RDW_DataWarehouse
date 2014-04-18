'''
Created on Jan 14, 2014

@author: sravi
'''

from database.generic_connector import setup_db_connection_from_ini
import os
from database.data_importer import import_csv_dir
import argparse
from sqlalchemy import Table, Column, select, MetaData
from sqlalchemy.engine import create_engine
import configparser
from database.connector import DBConnection
from sqlalchemy.orm import sessionmaker
from edschema.metadata.ed_metadata import generate_ed_metadata
from edcore.database import get_data_source_names
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection

SCHEMA_NAME = 'edware_ca_1_3'
STG_STAR_FACT_TABLE = 'tmp_fact_asmt_outcome'
LIVE_STAR_FACT_TABLE = 'fact_asmt_outcome'


RAW_FACT_MIGRATE_SQL = "Insert INTO {schema_name}.{live_Star_fact_table} (batch_guid, asmt_outcome_rec_id,asmt_rec_id,student_guid,state_code,district_guid,school_guid," \
          "section_guid,inst_hier_rec_id,section_rec_id,where_taken_id,where_taken_name,asmt_grade," \
          "enrl_grade,date_taken,date_taken_day,date_taken_month,date_taken_year,asmt_score,asmt_score_range_min," \
          "asmt_score_range_max,asmt_perf_lvl,asmt_claim_1_score,asmt_claim_1_score_range_min,asmt_claim_1_score_range_max," \
          "asmt_claim_2_score,asmt_claim_2_score_range_min,asmt_claim_2_score_range_max,asmt_claim_3_score," \
          "asmt_claim_3_score_range_min,asmt_claim_3_score_range_max,asmt_claim_4_score,asmt_claim_4_score_range_min," \
          "asmt_claim_4_score_range_max,status,most_recent,asmt_type,asmt_year,asmt_subject,gender,dmg_eth_hsp," \
          "dmg_eth_ami,dmg_eth_asn,dmg_eth_blk,dmg_eth_pcf,dmg_eth_wht,dmg_prg_iep,dmg_prg_lep,dmg_prg_504," \
          "dmg_prg_tt1,dmg_eth_derived) " \
          "select \'{fake_batch_guid}\' as batch_guid,{random_start_cnt}+fao.asmt_outcome_rec_id as asmt_outcome_rec_id,fao.asmt_rec_id," \
          "fao.student_guid,fao.state_code,fao.district_guid,fao.school_guid,fao.section_guid," \
          "fao.inst_hier_rec_id,fao.section_rec_id,fao.where_taken_id,fao.where_taken_name," \
          "fao.asmt_grade,fao.enrl_grade,fao.date_taken,fao.date_taken_day,fao.date_taken_month,fao.date_taken_year," \
          "fao.asmt_score,fao.asmt_score_range_min,fao.asmt_score_range_max," \
          "fao.asmt_perf_lvl,fao.asmt_claim_1_score,fao.asmt_claim_1_score_range_min,fao.asmt_claim_1_score_range_max," \
          "fao.asmt_claim_2_score,fao.asmt_claim_2_score_range_min,fao.asmt_claim_2_score_range_max," \
          "fao.asmt_claim_3_score,fao.asmt_claim_3_score_range_min,fao.asmt_claim_3_score_range_max," \
          "fao.asmt_claim_4_score,fao.asmt_claim_4_score_range_min,fao.asmt_claim_4_score_range_max,fao.status," \
          "fao.most_recent,fao.asmt_type,fao.asmt_year,fao.asmt_subject,fao.gender,fao.dmg_eth_hsp," \
          "fao.dmg_eth_ami,fao.dmg_eth_asn,fao.dmg_eth_blk,fao.dmg_eth_pcf,fao.dmg_eth_wht,fao.dmg_prg_iep," \
          "fao.dmg_prg_lep,fao.dmg_prg_504,fao.dmg_prg_tt1,fao.dmg_eth_derived " \
          "FROM {schema_name}.{stg_star_fact_table} as fao limit {limit}".format(schema_name=SCHEMA_NAME,
                                                                                 live_Star_fact_table=STG_STAR_FACT_TABLE,
                                                                                 fake_batch_guid='xxx-xxx-xxx',
                                                                                 random_start_cnt=99200002,
                                                                                 stg_star_fact_table=STG_STAR_FACT_TABLE,
                                                                                 limit=10)


def main():
    migrate_data()


def connect_db(db_driver, db_user, db_password, db_host, db_port, db_name):
    db_string = '{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(db_driver=db_driver,
                                                                                             db_user=db_user,
                                                                                             db_password=db_password,
                                                                                             db_host=db_host,
                                                                                             db_port=db_port,
                                                                                             db_name=db_name)
    engine = create_engine(db_string)
    return engine


def create_sqlalch_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session


def get_schema_metadata(db_engine, schema_name=None):
    metadata = MetaData()
    metadata.reflect(db_engine, schema_name)
    return metadata


def get_sqlalch_table_object(metadata, schema_name, table_name):
    table = metadata.tables[schema_name + '.' + table_name]
    return table


def migrate_fact(session, source_table, dest_table):
    print('migrating fact from: ' + str(source_table) + ' to ' + str(dest_table))
    #source_select_query = select([source_table]).limit(10)
    #result = session.execute(source_select_query)
    #for row in result:
    #    print(row)
    print(RAW_FACT_MIGRATE_SQL)
    session.execute(RAW_FACT_MIGRATE_SQL)
    session.commit()


def migrate_data():
    '''
    migrate all the data from staging to live star schema fact table
    '''
    engine = connect_db('postgresql+psycopg2', 'edware', 'edware2013', 'dbpgudl0.qa.dum.edwdc.net', 5432, 'edware')
    session = create_sqlalch_session(engine)
    metadata = get_schema_metadata(engine, SCHEMA_NAME)
    print(metadata.tables.keys())

    staging_star_fact = get_sqlalch_table_object(metadata, SCHEMA_NAME, STG_STAR_FACT_TABLE)
    live_star_fact = get_sqlalch_table_object(metadata, SCHEMA_NAME, LIVE_STAR_FACT_TABLE)

    migrate_fact(session, staging_star_fact, live_star_fact)


if __name__ == '__main__':
    main()
