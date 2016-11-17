"""This is the general JSON writer.

:author: nestep
:date: March 4, 2014
"""

import copy
import json

import data_generation.writers.util as writer_util


def write_object_to_file(path, layout, obj, root_path='out'):
    """For an object, create a new JSON file at the specified path and write the object to the path in JSON based on the
    provided layout. The object must have a 'get_object_set' method that returns a dictionary of objects whose
    attributes are available.

    :param path: The path to the CSV file
    :param layout: The layout specification of the JSON file
    :param obj: The object to write into the file
    :param root_path: The folder root for output file (optional, defaults to out/)
    """
    with open(root_path + '/' + path, 'w') as json_file:
        # By opening the file for writing, we implicitly delete any existing file contents
        # Create a copy of the layout to populate with data values
        out_layout = copy.deepcopy(layout)

        # Populate the layout
        writer_util.populate_json_layout(obj.get_object_set(), out_layout)

        # Write to file
        json.dump(out_layout, json_file)
