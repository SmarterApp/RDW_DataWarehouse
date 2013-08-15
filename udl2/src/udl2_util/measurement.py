'''
Define measurement and logging for new UDL's internal benchmarking.
Mostly using techniques from decorators in python

Created on June 10, 2013

Main Method: measure_cpu_time(function_to_be_decorated)
Main method: measure_elapsed_time(function_to_be_decorated)
Main method: measure_cpu_plus_elapsed_time(function_to_be_decorated)

@author: ejen
'''
import inspect
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import time
import datetime
from preetl import create_queries as queries

try:
    config_path_file = os.environ['UDL2_CONF']
except Exception:
    config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE

udl2_conf = imp.load_source('udl2_conf', config_path_file)
from udl2_conf import udl2_conf


def remove_celery_system_frame_objects(frames):
    '''
    a function that removes frame objects that is part of celery system. So we keep only UDL2 related calling
    @param frames: a list of frames names
    @type frames: list
    '''
    udl2_frames = [f for f in frames if '/celery/' not in f and '<frozen ' not in f and '/billiard/' not in f and '/kombu/' not in f and 'measurement.py:_wrapped' not in f and
                   '/celery:<module>' not in f]
    return udl2_frames


def measure_cpu_time(fn, quiet=udl2_conf['quiet_mode']):
    '''
    a decorator measure cpu process time for executing fn and print out the result to standard output
    @param fn: function that are to be executed
    @type fn: a funtion in python
    '''
    def _wrapped(*args, **kwargs):
        if quiet:
            return fn(*args, **kwargs)
        else:
            start_cpu_time = time.clock()
            result = fn(*args, **kwargs)
            end_cpu_time = time.clock()
            current_frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(current_frame, 1)
            frames = [fn.__name__] + [of[1] + ':' + of[3] for of in outer_frames]
            frames = remove_celery_system_frame_objects(frames)
            print("MEASURE-- cpu time {time:.10f} seconds for executing {module:s}.{function:s}".format(time=(end_cpu_time - start_cpu_time),
                                                                                                        module=fn.__module__,
                                                                                                        function=fn.__name__,))
            return result
    return _wrapped


def measure_elapsed_time(fn, quiet=udl2_conf['quiet_mode']):
    '''
    a decorator measure elasped time for executing fn and print out the result to standard output
    @param fn: function that are to be executed
    @type fn: a funtion in python
    '''
    def _wrapped(*args, **kwargs):
        if quiet:
            return fn(*args, **kwargs)
        else:
            start_time = time.time()
            result = fn(*args, **kwargs)
            end_time = time.time()
            current_frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(current_frame, 1)
            frames = [fn.__name__] + [of[1] + ':' + of[3] for of in outer_frames]
            frames = remove_celery_system_frame_objects(frames)
            print("MEASURE-- elapsed time {time:.10f} seconds for executing {module:s}.{function:s}".format(time=(end_time - start_time),
                                                                                                            module=fn.__module__,
                                                                                                            function=fn.__name__,))
            return result
    return _wrapped


def measure_cpu_plus_elasped_time(fn, quiet=udl2_conf['quiet_mode']):
    '''
    a decorator measure elasped time for executing fn and print out the result to standard output
    @param fn: function that are to be executed
    @type fn: a funtion in python
    '''
    def _wrapped(*args, **kwargs):
        if quiet:
            return fn(*args, **kwargs)
        else:
            start_time = time.time()
            start_clock = time.clock()
            result = fn(*args, **kwargs)
            end_clock = time.clock()
            end_time = time.time()
            current_frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(current_frame, 1)
            frames = [fn.__name__] + [of[1] + ':' + of[3] for of in outer_frames]
            frames = remove_celery_system_frame_objects(frames)
#             print(("MEASURE-- " +
#                   #" call stack: {frame}, " +
#                   " cpu time: {ctime:.10f} seconds, elapsed time: {etime:.10f} seconds " +
#                   " for executing {module:s}.{function:s}, args: {args},kwargs: {kwargs}").format(frame=" <== ".join(frames),
#                                                                                                  etime=(end_time - start_time),
#                                                                                                  module=fn.__module__,
#                                                                                                  ctime=(end_clock - start_clock),
#                                                                                                  function=fn.__name__,
#                                                                                                  args=args,
#                                                                                                  kwargs=kwargs))
            return result
    return _wrapped


def show_amount_of_data_affected(fn, quiet=udl2_conf['quiet_mode']):
    '''
    a decorator to print normalized message for amount of data to be moved
    @param fn: function that are to be executed
    @type fn: a funtion in python that return amount of data be moved, it returns a dictionary with following fields {amount: number of data,
            unit: measure unit, module: where the code module is, function: what function is used}
    '''
    def _wrapped(*args, **kwargs):
        if quiet:
            return fn(*args, **kwargs)
        else:
            result = fn(*args, **kwargs)
            current_frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(current_frame, 1)
            frames = [fn.__name__] + [of[1] + ':' + of[3] for of in outer_frames]
            frames = remove_celery_system_frame_objects(frames)
#             print(("MEASURE--  call stack: {frame}, " +
#                   "{amount:s} {unit:s} are {action:s} by {module:s}.{function:s}").format(frame=" <== ".join(frames),
#                                                                                           amount=str(result['amount']),
#                                                                                           unit=result['unit'],
#                                                                                           action=result['action'],
#                                                                                           module=result['module'],
#                                                                                           function=result['function']))
#             return result
    return _wrapped


def describe_tasks(fn):
    pass


def benchmarking_udl2(func):
    '''
    Decorator for benchmarking UDL2 stages (Worker level)
    '''
    def wrapper_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        from udl2 import message_keys as mk
        # add guid batch
        result[mk.GUID_BATCH] = args[0][mk.GUID_BATCH]
        # add load_type
        result[mk.LOAD_TYPE] = args[0][mk.LOAD_TYPE]
        # add phase name
        result[mk.UDL_PHASE] = str(func.__module__) + '.' + str(func.__name__)
        # insert result into batch table
        record_benchmark_in_batch_table(start_time, end_time, result)
        return result
    return wrapper_func


def record_benchmark_in_batch_table(start_time, end_time, result):
    # TODO: should use try-except
    if result is None:
        return

    from udl2 import message_keys as mk
    # add time
    result[mk.DURATION] = str(end_time - start_time)
    result[mk.START_TIMESTAMP] = str(start_time)
    result[mk.END_TIMESTAMP] = str(end_time)
    # add status, by default is SUCCESS
    if mk.UDL_PHASE_STEP_STATUS not in list(result.keys()):
        result[mk.UDL_PHASE_STEP_STATUS] = mk.SUCCESS
    # add udl_leaf, by default is False
    if mk.UDL_LEAF not in list(result.keys()):
        result[mk.UDL_LEAF] = False

    # insert into batch table
    from udl2.celery import celery, udl2_conf
    from udl2_util.database_util import connect_db, execute_queries

    insert_query = queries.insert_batch_row_query(udl2_conf['udl2_db']['staging_schema'], result[mk.GUID_BATCH], **result)

    # create database connection
    (conn, _engine) = connect_db(udl2_conf['udl2_db']['db_driver'],
                                 udl2_conf['udl2_db']['db_user'],
                                 udl2_conf['udl2_db']['db_pass'],
                                 udl2_conf['udl2_db']['db_host'],
                                 udl2_conf['udl2_db']['db_port'],
                                 udl2_conf['udl2_db']['db_database'])
    # insert into batch table
    execute_queries(conn, [insert_query], 'Exception in record_benchmark_in_batch_table, execute query to insert into batch table', 'measurement', 'record_benchmark_in_batch_table')
    conn.close()
