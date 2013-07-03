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
