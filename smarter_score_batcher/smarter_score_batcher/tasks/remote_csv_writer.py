from smarter_score_batcher.celery import celery
from smarter_score_batcher.processing.file_processor import generate_csv_from_xml
from smarter_score_batcher.error.exceptions import TSBException
from smarter_score_batcher.error.error_handler import handle_error
from smarter_score_batcher.utils.metadata_generator import metadata_generator_task


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(meta, csv_file_path, xml_file_path, work_dir, metadata_queue):
    '''
    celery task to generate csv from given xml path
    :param csv_file_path: csv file path
    :param xml_file_path: xml file path
    :returns: True when file is written
    '''
    rtn = False
    try:
        metadata_generator_task.apply_async(args=(xml_file_path,), queue=metadata_queue)
        mode = 0o700
        rtn = generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir, metadata_queue, mode=mode)
    except TSBException as e:
        # all TSB exception should be caught in here
        e.err_input = 'student_guid: ' + meta.student_id
        handle_error(e, meta.state_code, meta.asmt_id)
    return rtn
