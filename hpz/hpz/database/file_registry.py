from datetime import datetime
import logging
from uuid import uuid4
from hpz.database.constants import DatabaseConstants
from hpz.database.hpz_connector import get_hpz_connection

__author__ = 'okrook'

logger = logging.getLogger(__name__)


class FileRegistry:

    @staticmethod
    def register_request(user_id):
        registration_id = uuid4()
        registration_info = {DatabaseConstants.REGISTRATION_ID: str(registration_id), DatabaseConstants.USER_ID: user_id}

        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            conn.execute(file_reg_table.insert().values(registration_info))

        return registration_id

    @staticmethod
    def update_registration(registration_id, file_path, file_name):
        registration_info = {DatabaseConstants.FILE_PATH: file_path,
                             DatabaseConstants.CREATE_DT: datetime.now(),
                             DatabaseConstants.FILE_NAME: file_name}

        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            result = conn.execute(file_reg_table.update().where(file_reg_table.c.registration_id == registration_id).values(registration_info))

            return result.rowcount > 0

    @staticmethod
    def get_registration_info(registration_id):
        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            result = conn.execute(file_reg_table.select().where(file_reg_table.c.registration_id == registration_id))

            registration_info = result.fetchone()

            return registration_info

    @staticmethod
    def is_file_registered(registration_id):
        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            result = conn.execute(file_reg_table.select(limit=1).where(file_reg_table.c.registration_id == registration_id))

            return result.rowcount == 1
