import os

from udl2.celery import celery
from celery.utils.log import get_task_logger
from filedecrypter.file_decrypter import decrpyt_file
import udl2.message_keys as mk

__author__ = 'swimberly'

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_decrypter.task")
def task(incoming_msg):
    file_to_decrypt = incoming_msg[mk.FILE_TO_DECRYPT]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    passphrase = incoming_msg[mk.PASSPHRASE]
    gpghome = None

    decrypted_file = decrypt_file(file_to_decrypt, lzw, passphrase, gpghome)
    logger.info('Decrypted file:', decrypted_file)


