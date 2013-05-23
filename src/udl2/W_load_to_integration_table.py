'''
Created on May 22, 2013

@author: ejen
'''
from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import move_to_target.column_mapping as col_map
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
import datetime


logger = get_task_logger(__name__)


#*************implemented via chord*************
@celery.task(name="udl2.W_load_to_integration_table.task")
def task(batch):
    conf = generate_conf(batch)
    move_data_from_staging_to_integration(conf)
    return batch


def generate_conf(msg):
    conf = {
             # add batch_id from msg
            'batch_id': msg['batch_id'],
            # error schema
            'error_schema': udl2_conf['udl2_db']['staging_schema'],
            # source schema
            'source_schema': udl2_conf['udl2_db']['staging_schema'],
            # source database setting
            'db_host_source': udl2_conf['udl2_db']['db_host'],
            'db_port_source': udl2_conf['udl2_db']['db_port'],
            'db_user_source': udl2_conf['udl2_db']['db_user'],
            'db_name_source': udl2_conf['udl2_db']['db_database'],
            'db_password_source': udl2_conf['udl2_db']['db_pass'],
            'db_driver_source': udl2_conf['udl2_db']['db_driver'],

            # target schema
            'target_schema': udl2_conf['udl2_db']['integration_schema'],
            # target database setting
            'db_host_target': udl2_conf['udl2_db']['db_host'],
            'db_port_target': udl2_conf['udl2_db']['db_port'],
            'db_user_target': udl2_conf['udl2_db']['db_user'],
            'db_name_target': udl2_conf['udl2_db']['db_database'],
            'db_password_target': udl2_conf['udl2_db']['db_pass'],
    }
    return conf