'''
Created on May 22, 2013

@author: ejen
'''
from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import move_to_target.column_mapping as col_map
from move_to_integration import move_data_from_staging_to_integration
import datetime


logger = get_task_logger(__name__)


#*************implemented via chord*************
@celery.task(name="udl2.W_move_to_integration.task")
def task(msg):
    pass