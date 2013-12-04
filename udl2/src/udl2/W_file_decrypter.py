from udl2.celery import celery
from celery import Task
from celery.utils.log import get_task_logger
from filedecrypter.file_decrypter import decrypt_file
import udl2.message_keys as mk
from udl2.celery import udl2_conf
from udl2_util.measurement import BatchTableBenchmark
import datetime
from udl2.udl2_base_task import Udl2BaseTask


__author__ = 'sravi'

'''
File Decrypter Worker for the UDL Pipeline.
The file arrived at zones/landing/work/<TENANT>/<TS_GUID_BATCH>/arrived/ is decrypted
and written to zones/landing/work/<TENANT>/<TS_GUID_BATCH>/decrypted/

The output of this worker will serve as the input to the subsequent worker [W_file_expander].
'''

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_decrypter.task", base=Udl2BaseTask)
def task(incoming_msg):
    """
    This is the celery task to decrypt the source file
    """
    start_time = datetime.datetime.now()
    file_to_decrypt = incoming_msg[mk.FILE_TO_DECRYPT]
    passphrase = udl2_conf['passphrase']
    guid_batch = incoming_msg[mk.GUID_BATCH]
    gpghome = udl2_conf['gpg_home']
    tenant_directory_paths = incoming_msg[mk.TENANT_DIRECTORY_PATHS]
    decrypt_to_dir = tenant_directory_paths[mk.DECRYPTED]
    load_type = incoming_msg[mk.LOAD_TYPE]

    logger.info('W_FILE_DECRYPTER: received file <%s> with guid_batch = <%s>' % (file_to_decrypt, guid_batch))
    logger.info('W_FILE_DECRYPTER: Decrypt to <%s>' % decrypt_to_dir)

    status, decrypted_file = decrypt_file(file_to_decrypt, decrypt_to_dir, passphrase, gpghome)
    logger.info('Decrypted file:', decrypted_file)
    logger.info('Decryption status:', status)

    finish_time = datetime.datetime.now()

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, finish_time, task_id=str(task.request.id))
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file expander
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({mk.FILE_TO_EXPAND: decrypted_file})
    return outgoing_msg