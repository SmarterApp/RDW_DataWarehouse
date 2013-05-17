from __future__ import absolute_import
from udl2.celery import celery
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
    print('I am the exploder, about to copy data from staging table into target star schema')

    # temporary
    conf = generate_conf()

    # get column mapping
    column_map = col_map.get_column_mapping()
    fact_table = col_map.get_target_table_callback()

    # reference: http://docs.celeryproject.org/en/master/userguide/canvas.html#chords
    # define callback
    callback = explode_data_to_fact_table.s(conf=conf, fact_table=fact_table, column_map=column_map[fact_table])
    # define tasks which can be done in parallel
    header = []
    for dim_table in col_map.get_target_tables_parallel():
        header.append(explode_data_to_dim_table.subtask((conf, dim_table, column_map[dim_table])))
    chord(header)(callback)

    """
    udl2.W_final_cleanup.task.apply_async([msg],
                                            queue='Q_final_cleanup',
                                            routing_key='udl2')
    """


@celery.task(name="udl2.W_move_to_target.task1")
def explode_data_to_dim_table(conf, dim_table, column_mapping):
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
def generate_conf():
    conf = {
            # TBD
            'source_table': 'STG_SBAC_ASMT_OUTCOME',
            'source_schema': 'udl2',
            'target_schema': 'edware',

            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'udl2',
            'db_name': 'udl2',
            'db_password': 'udl2abc1234',
    }
    return conf
