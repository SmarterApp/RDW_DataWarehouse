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

from __future__ import absolute_import
import datetime
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.move_to_target.move_to_target import move_data_from_int_tables_to_target_table
from edudl2.move_to_target.move_to_target_setup import generate_conf
from edudl2.udl2.constants import Constants
from edudl2.udl2_util.util import merge_to_udl2stat_notification

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_load_sr_integration_to_target.task', base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info("LOAD_SR_INTEGRATION_TO_TARGET: Migrating data from SR integration tables to target tables.")
    guid_batch = msg[mk.GUID_BATCH]
    load_type = msg[mk.LOAD_TYPE]

    source_tables = [Constants.UDL2_INTEGRATION_TABLE(load_type), Constants.UDL2_JSON_INTEGRATION_TABLE(load_type)]
    target_table = Constants.SR_TARGET_TABLE

    target_schema = msg[mk.TARGET_DB_SCHEMA] if mk.TARGET_DB_SCHEMA in msg else msg[mk.GUID_BATCH]
    conf = generate_conf(guid_batch, msg[mk.PHASE], load_type, msg[mk.TENANT_NAME], target_schema)
    affected_rows = move_data_from_int_tables_to_target_table(conf, task.name, source_tables, target_table)

    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, end_time, task_id=str(task.request.id),
                                    working_schema="", size_records=affected_rows[0], tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()

    notification_data = {mk.TOTAL_ROWS_LOADED: affected_rows[0]}
    merge_to_udl2stat_notification(guid_batch, notification_data)
    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update(notification_data)
    return outgoing_msg
