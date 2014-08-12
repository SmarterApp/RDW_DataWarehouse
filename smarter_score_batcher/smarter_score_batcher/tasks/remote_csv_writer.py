from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.file_utils import csv_file_writer


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_write(path, data):
    return csv_file_writer(path, data)
