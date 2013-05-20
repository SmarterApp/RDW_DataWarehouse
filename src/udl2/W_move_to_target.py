from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import move_to_target.column_mapping as col_map
from move_to_target.move_to_target import explode_data_to_one_table
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
    conf = generate_conf(msg, col_map.get_target_table_callback()[1])

    # get column mapping
    column_map = col_map.get_column_mapping()
    fact_table = col_map.get_target_table_callback()[0]

    # reference: http://docs.celeryproject.org/en/master/userguide/canvas.html#chords
    # define callback
    callback = explode_data_to_fact_table.s(conf=conf, fact_table=fact_table, column_map=column_map[fact_table])
    # define tasks which can be done in parallel
    header = []
    for dim_table, source_table in col_map.get_target_tables_parallel().items():
        print(dim_table, source_table)
        conf['source_table'] = source_table
        header.append(explode_data_to_dim_table.subtask((conf, dim_table, column_map[dim_table])))
    chord(header)(callback)

    """
    # the next stage is 'clean_up', it will be defined in Chain after current task
    udl2.W_final_cleanup.task.apply_async([msg],
                                            queue='Q_final_cleanup',
                                            routing_key='udl2')
    """


@celery.task(name="udl2.W_move_to_target.task1")
def explode_data_to_dim_table(conf, dim_table, column_mapping):
    print(column_mapping)
    explode_data_to_one_table(conf, dim_table, column_mapping)


@celery.task(name="udl2.W_move_to_target.task2")
def explode_data_to_fact_table(result_from_parallel, conf, fact_table, column_map):
    print('I am the exploder, about to copy fact table')
    explode_data_to_one_table(conf, fact_table, column_map)
    print('I am the exploder, copied data from staging table into target star schema at %s' % str(datetime.datetime.now()))


@celery.task(name="udl2.W_move_to_target.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


# will be replaced by conf file
def generate_conf(msg, source_table):
    conf = {
            # These three values can be replaced by reading from configuration file or msg
            # source_table is integration table
            'source_table': source_table,
            'source_schema': 'udl2',
            'target_schema': 'edware',

            # add info from msg
            'batch_id': msg['batch_id'],

            # database setting
            'db_host': udl2_conf['postgresql']['db_host'],
            'db_port': udl2_conf['postgresql']['db_port'],
            'db_user': udl2_conf['postgresql']['db_user'],
            'db_name': udl2_conf['postgresql']['db_database'],
            'db_password': udl2_conf['postgresql']['db_pass'],
    }
    return conf
