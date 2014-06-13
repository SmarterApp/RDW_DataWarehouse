"""
Generate IDs that conform to student registration (SBAC) requirements.

@author: nestep
@date: February 22, 2014
"""

import multiprocessing

from uuid import uuid4


class IDGen():
    def __init__(self, lock=multiprocessing.Lock(), rec_dict={}):
        self._start_rec_id = 100000000000
        self._rec_id_lock = lock
        self._rec_id_dict = rec_dict
        self._rec_id = multiprocessing.Value('i', 100000000000)

    def get_rec_id(self, type_str):
        """
        Get the next integer record ID within the system for the given type string.

        @param type_str: The type string to get a record ID for
        @returns: Next ID for the given type string
        """
        with self._rec_id_lock:
            if type_str not in self._rec_id_dict:
                self._rec_id_dict[type_str] = self._start_rec_id
            nid = self._rec_id_dict[type_str]
            self._rec_id_dict[type_str] += 1
        return nid

    @staticmethod
    def get_uuid():
        """
        Get a UUID.

        @returns: New UUID
        """
        return str(uuid4())

    @staticmethod
    def get_sr_uuid():
        """
        Get a UUID that conforms to student registration requirements.

        @returns: New UUID for student registration
        """
        return uuid4().hex[:30]
