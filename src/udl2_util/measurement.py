'''
Define measurement and logging for new UDL's internal benchmarking.
Mostly using techniques from decorators in python

Created on June 10, 2013

Main Method: measure_cpu_time(function_to_be_decorated)
Main method: measure_elapsed_time(function_to_be_decorated)

@author: ejen
'''
import time


def measure_cpu_time(fn):
    
    def _wrapped(*args, **kwargs):
        start_cpu_time = time.clock()
        fn(*args, **kwargs)
        end_cpu_time = time.clock()
        print("cpu time {time} seconds for executing {function}".format(time=end_cpu_time - start_cpu_time,
                                                                function=fn.__name__))
    return _wrapped


def measure_elasped_time(fn):
    
    def _wrapped(*args, **kwargs):
        start_time = time.time()
        fn(*args, **kwargs)
        end_time = time.time()
        print("elapsed time {time} seconds for executing {function}".format(time=end_time - start_time,
                                                                    function=fn.__name__))
    return _wrapped
