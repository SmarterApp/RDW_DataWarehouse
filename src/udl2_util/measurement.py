'''
Define measurement and logging for new UDL's internal benchmarking.
Mostly using techniques from decorators in python

Created on June 10, 2013

Main Method: measure_cpu_time(function_to_be_decorated)
Main method: measure_elapsed_time(function_to_be_decorated)
Main method: measure_cpu_plus_elapsed_time(function_to_be_decorated)

@author: ejen
'''
import time


def measure_cpu_time(fn, quite=True):
    '''
    a decorator measure cpu process time for executing fn and print out the result to standard error
    @param fn: function that are to be executed
    @type fn: a funtion in python
    '''
    def _wrapped(*args, **kwargs):
        if quite:
            return fn(*args, **kwargs)
        else:
            start_cpu_time = time.clock()
            result = fn(*args, **kwargs)
            end_cpu_time = time.clock()
            print("cpu time {time} seconds for executing {function}".format(time=(end_cpu_time - start_cpu_time),
                                                                                       function=fn.__name__,))
            return result   
    return _wrapped


def measure_elapsed_time(fn, quite=True):
    '''
    a decorator measure elasped time for executing fn and print out the result to standard error
    @param fn: function that are to be executed
    @type fn: a funtion in python
    '''
    def _wrapped(*args, **kwargs):
        if quite:
            return fn(*args, **kwargs)
        else:
            start_time = time.time()
            result = fn(*args, **kwargs)
            end_time = time.time()
            print("elapsed time {time} seconds for executing {function}".format(time=(end_time - start_time),
                                                                                function=fn.__name__,))
            return result
    return _wrapped


def measure_cpu_plus_elasped_time(fn, quite=True):
    '''
    a decorator measure elasped time for executing fn and print out the result to standard error
    @param fn: function that are to be executed
    @type fn: a funtion in python
    '''
    def _wrapped(*args, **kwargs):
        if quite:
            return fn(*args, **kwargs)
        else:
            start_time = time.time()
            start_clock = time.clock()
            result = fn(*args, **kwargs)
            end_clock = time.clock()
            end_time = time.time()
            print("cpu time {ctime} seconds, elapsed time {etime} seconds for executing {function}".format(etime=(end_time - start_time),
                                                                                                           ctime=(end_clock - start_clock),
                                                                                                           function=fn.__name__,))
            return result
    return _wrapped
