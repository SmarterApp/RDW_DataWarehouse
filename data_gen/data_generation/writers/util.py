"""Utility functions for the general writers module.

:author: nestep
:date: February 24, 2014
"""

from data_generation import run_id as global_run_id

import data_generation.util.id_gen as id_gen


def build_csv_row_values(root_obj, columns, filters=None, tbl_name=None):
    """Build a value list for a single CSV row of data.

    :param root_obj: The set of objects to find attributes values within
    :param columns: CSV file column definition
    :param filters: Filters to apply to values (optional)
    :param tbl_name: Name of table this row is being generated for (optional)
    :returns: List of values for single row in CSV file
    """
    # Go through columns
    values = []
    for column in columns:
        val = _get_attr_value(column['val'], root_obj, tbl_name)

        # Put the value into the result list
        if filters is not None and 'filter' in column:
            if column['filter'] not in filters:
                raise KeyError("Unknown filter '" + column['filter'] + "' found for column '" + column['name'] + "'")
            else:
                val = filters[column['filter']](val)
        values.append(val)

    # Return the result
    return values


def populate_json_layout(root_obj, layout):
    """Populate a layout with data values for a JSON file. This will populate the layout parameter in-place.

    :param root_obj: The set of objects to find attribute values within
    :param layout: JSON file layout to populate
    :returns: A populated JSON layout
    """
    # Traverse layout
    for key, value in layout.items():
        if type(value) is dict:
            populate_json_layout(root_obj, value)
        else:
            attr_val = _get_attr_value(value, root_obj)
            layout[key] = attr_val if attr_val is not None else ''


def _get_attr_value(attr_path, obj=None, tbl_name=None):
    """Traverse an object, following a list of tokens, and get the desired attribute value. This will skip the first
    part of the attribute path as that part is assumed to be the passed object, except for the following special values:
      - '': return None
      - 'UNIQUE_ID': return new UUID
      - 'UNIQUE_REC_ID': return next record ID in system
      - 'BATCH_GUID': return GUID for batch
      - Without '.': return the attribute path, assumed to be a string literal

    :param attr_path: The path to traverse within an object
    :param obj: The object to start looking for attribute values within
    :param tbl_name: Name of table this row is being generated for (optional)
    :returns: Value of attribute or None if not found
    """
    # Determine if attr_path is special value
    if attr_path == '':
        return None
    elif attr_path == 'UNIQUE_ID':
        return id_gen.get_uuid()
    elif 'UNIQUE_REC_ID' in attr_path:
        if tbl_name is None:
            return id_gen.get_rec_id('global_unique')
        else:
            return id_gen.get_rec_id(tbl_name)
    elif attr_path == 'BATCH_GUID':
        return global_run_id
    elif not '.' in attr_path:
        return attr_path
    elif obj is None:
        return None

    # Tokenize the attribute path
    tokens = attr_path.split('.')

    # Traverse
    for i, tok in enumerate(tokens):
        isdict = isinstance(obj, dict)
        if (isdict and obj[tok] is None) or (not isdict and getattr(obj, tok, None) is None):
            # Blank the value and exit traversal
            return None
        obj = obj[tok] if isdict else getattr(obj, tok)
    return obj
