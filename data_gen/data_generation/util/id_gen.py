"""Generate IDs for various things.

:author: nestep
:date: February 22, 2014
"""

from uuid import uuid4

__next_ids = {}
__start_rec_id = 20


def get_rec_id(type_str):
    """Get the next integer record ID within the system for the given type string.

    :param type_str: The type string to get a record ID for
    :returns: Next ID for the given type string
    """
    global __next_ids
    if type_str not in __next_ids:
        __next_ids[type_str] = __start_rec_id
    nid = __next_ids[type_str]
    __next_ids[type_str] += 1
    return nid


def get_uuid():
    """Get a UUID.

    :returns: New UUID
    """
    return str(uuid4())
