'''
Created on Mar 21, 2014

@author: tosako
'''
from kombu.entity import Exchange, Queue
from edmigrate.utils.constants import Constants


exchange = Exchange(Constants.CONDUCTOR_EXCHANGE, type='direct')
queue = Queue(Constants.CONDUCTOR_QUEUE, exchange=exchange, routing_key=Constants.CONDUCTOR_ROUTING_KEY, durable=False, auto_delete=True)
