from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import move_to_target.column_mapping as col_map
from move_to_target.move_to_target import explode_data_to_dim_table, explode_data_to_fact_table, get_table_column_types
from celery import chord
import datetime
import udl2.W_final_cleanup


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_move_to_target.task")
def task(msg):
    logger.info(task.name)
    # logger.info('Moving data from %s into target' % msg['source_table'])
    print('*****I am the exploder, about to copy data from staging table into target star schema %s' % str(msg))

    # generate conf info, including db settings and batch_id, source_table, source_schema, target_schema
    conf = generate_conf(msg)

    # get column mapping
    column_map = col_map.get_column_mapping()
    fact_table, source_table_for_fact_table = col_map.get_target_table_callback()

    # get column types
    column_types = get_table_column_types(conf, fact_table, list(column_map[fact_table].keys()))

    # reference: http://docs.celeryproject.org/en/master/userguide/canvas.html#chords
    # define callback
    callback = explode_data_to_fact_table_task.s(conf=conf, source_table=source_table_for_fact_table, fact_table=fact_table, column_map=column_map[fact_table], column_types=column_types)
    # define tasks which can be done in parallel
    header = []
    for dim_table, source_table in col_map.get_target_tables_parallel().items():
        column_types = get_table_column_types(conf, dim_table, list(column_map[dim_table].keys()))
        header.append(explode_data_to_dim_table_task.subtask((conf, source_table, dim_table, column_map[dim_table], column_types)))
    chord(header)(callback)

    """
    # the next stage is 'clean_up', it will be defined in Chain after current task
    udl2.W_final_cleanup.task.apply_async([msg],
                                            queue='Q_final_cleanup',
                                            routing_key='udl2')
    """


@celery.task(name="udl2.W_move_to_target.task1")
def explode_data_to_dim_table_task(conf, source_table, dim_table, column_mapping, column_types):
    explode_data_to_dim_table(conf, conf['db_user'], conf['db_password'], conf['db_host'], conf['db_name'],
                              source_table, dim_table, column_mapping, column_types)


@celery.task(name="udl2.W_move_to_target.task2")
def explode_data_to_fact_table_task(result_from_parallel, conf, source_table, fact_table, column_map, column_types):
    print('I am the exploder, about to copy fact table')
    explode_data_to_fact_table(conf, conf['db_user_target'], conf['db_password_target'],
                              conf['db_host_target'], conf['db_name_target'],
                              source_table, fact_table, column_map, column_types)
    print('I am the exploder, copied data from staging table into target star schema at %s' % str(datetime.datetime.now()))


@celery.task(name="udl2.W_move_to_target.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


# will be replaced by conf file
def generate_conf(msg):
    conf = {
             # add batch_id from msg
            'batch_id': msg['batch_id'],

            # source schema
            'source_schema': udl2_conf['udl2_db']['integration_schema'],
            # source database setting
            'db_host': udl2_conf['postgresql']['db_host'],
            'db_port': udl2_conf['postgresql']['db_port'],
            'db_user': udl2_conf['postgresql']['db_user'],
            'db_name': udl2_conf['postgresql']['db_database'],
            'db_password': udl2_conf['postgresql']['db_pass'],

            # target schema
            'target_schema': udl2_conf['target_db']['db_schema'],
            # target database setting
            'db_host_target': udl2_conf['target_db']['db_host'],
            'db_port_target': udl2_conf['target_db']['db_port'],
            'db_user_target': udl2_conf['target_db']['db_user'],
            'db_name_target': udl2_conf['target_db']['db_database'],
            'db_password_target': udl2_conf['target_db']['db_pass'],
    }
    return conf
