from uuid import uuid4
from hpz.database.hpz_connector import get_hpz_connection

__author__ = 'okrook'


class FileRegistry:

    @staticmethod
    def register_request():
        registration_id = uuid4()
        registration_info = {'uuid': str(registration_id)}

        with get_hpz_connection() as conn:
            file_reg_table = conn.get_table(table_name='file_registry')
            conn.execute(file_reg_table.insert().values(registration_info))

        return registration_id

    @staticmethod
    def register_file(registration_id, file_path):
        pass
