from datetime import datetime
from uuid import uuid4
from hpz.database.constants import DatabaseConstants
from hpz.database.hpz_connector import get_hpz_connection

__author__ = 'okrook'


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
    def register_file(registration_id, file_path):
        registration_info = {DatabaseConstants.FILE_PATH: file_path,
                             DatabaseConstants.CREATION_DATE: datetime.date()}

        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name=DatabaseConstants.HPZ_TABLE)
            conn.execute(file_reg_table.update().where(file_reg_table.c.registration_id == registration_id).values(registration_info))

    @staticmethod
    def get_file_path(registration_id):
        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name='file_registry')
            registration_info = conn.execute(file_reg_table.select().where(file_reg_table.c.uuid == registration_id))

            return registration_info['file_path']
