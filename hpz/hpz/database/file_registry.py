from datetime import datetime
import logging
from uuid import uuid4
from sqlalchemy.sql.expression import exists, select
from hpz.database.constants import DatabaseConstants
from hpz.database.hpz_connector import get_hpz_connection

__author__ = 'okrook'

logger = logging.getLogger(__name__)


class FileRegistry:

    @staticmethod
    def register_request():
        registration_id = uuid4()
        registration_info = {DatabaseConstants.REGISTRATION_ID: str(registration_id)}

        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            conn.execute(file_reg_table.insert().values(registration_info))

        return registration_id

    @staticmethod
    def file_upload_request(registration_id, file_path):
        registration_info = {DatabaseConstants.FILE_PATH: file_path,
                             DatabaseConstants.CREATION_DATE: datetime.now()}

        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            conn.execute(file_reg_table.update().where(file_reg_table.c.registration_id == registration_id).values(registration_info))

    @staticmethod
    def get_file_path(registration_id):
        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name='file_registry')
            result = conn.execute(file_reg_table.select().where(file_reg_table.c.registration_id == registration_id))

            registration_info = result.fetchone()

            return registration_info['file_path']

    @staticmethod
    def is_file_registered(registration_id):
        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name='file_registry')
            result = conn.execute(file_reg_table.select(exists(select([file_reg_table.c.registration_id]).where(file_reg_table.c.registration_id == registration_id))))

            return result
