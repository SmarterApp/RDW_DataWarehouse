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
import datetime
import time
import logging
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.udl2.constants import Constants

logger = logging.getLogger(__name__)

# try:
#     config_path_file = os.environ['UDL2_CONF']
# except Exception:
#     config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
#
# udl2_conf = imp.load_source('udl2_conf', config_path_file)
# from udl2_conf import udl2_conf


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


class BatchTableBenchmark(object):
    '''
    Class for maintaining the information required to populate the batch table
    '''

    def __init__(self, guid_batch, load_type, udl_phase, start_timestamp, end_timestamp=datetime.datetime.now(), working_schema=None, size_records=None, size_units=None,
                 udl_phase_step_status=mk.SUCCESS, udl_phase_step=None, udl_leaf=False, task_id=None, task_status_url=None, user_email=None, user_sid=None,
                 error_desc=None, stack_trace=None, tenant='', input_file=''):
        '''Constructor'''
        self.guid_batch = guid_batch
        self.load_type = load_type
        self.udl_phase = udl_phase
        self.start_timestamp = str(start_timestamp)
        self.end_timestamp = str(end_timestamp)
        self.duration = str(end_timestamp - start_timestamp)
        self.working_schema = working_schema
        self.size_records = size_records
        self.size_units = size_units
        self.udl_phase_step_status = udl_phase_step_status
        self.udl_phase_step = udl_phase_step
        self.udl_leaf = udl_leaf
        self.task_id = task_id
        self.task_status_url = task_status_url
        self.user_email = user_email
        self.user_sid = user_sid
        self.error_desc = error_desc
        self.stack_trace = stack_trace
        self.tenant = tenant
        self.input_file = input_file

    def get_result_dict(self):
        '''
        Get a dictionary containing all instance attributes that are not None
        '''
        return {col: val for col, val in self.__dict__.items() if val is not None}

    def record_benchmark(self):
        '''
        Record the benchmark information for the this instance of the benchmarking information
        '''

        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            connector.execute(batch_table.insert(), self.get_result_dict())
