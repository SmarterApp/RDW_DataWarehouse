from celery.utils.log import get_task_logger
import datetime
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2.celery import celery
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.celery import udl2_conf
from edudl2.filedecrypter.file_decrypter import decrypt_file
from edudl2.udl2_util.measurement import BatchTableBenchmark

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

    logger.info('W_FILE_DECRYPTER: received file {file} with guid_batch {guid_batch}'.format(file=file_to_decrypt,
                                                                                             guid_batch=guid_batch))
    logger.info('W_FILE_DECRYPTER: Decrypt to {dir}'.format(dir=decrypt_to_dir))

    status, decrypted_file = decrypt_file(file_to_decrypt, decrypt_to_dir, passphrase, gpghome)
    logger.info('Decrypted file: {file}'.format(file=decrypted_file))
    logger.info('Decryption status: {status}'.format(status=str(status)))

    finish_time = datetime.datetime.now()

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, finish_time, task_id=str(task.request.id), tenant=incoming_msg[mk.TENANT_NAME])
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file expander
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({mk.FILE_TO_EXPAND: decrypted_file})
    return outgoing_msg
