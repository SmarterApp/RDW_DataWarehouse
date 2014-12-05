
from smarter_score_batcher.celery import celery
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up


@celery.task(name="tasks.tsb.remote_metadata_writer")
def metadata_generator_task(file_path):
    metadata_generator_bottom_up(file_path, generateMetadata=True)
