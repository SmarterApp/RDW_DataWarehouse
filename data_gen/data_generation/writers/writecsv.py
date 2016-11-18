"""This is the general CSV writer.

:author: nestep
:date: February 24, 2014
"""

import csv

import data_generation.writers.datefilters as writers_filters
import data_generation.writers.util as writers_util


available_filters = writers_filters.FILTERS


def register_filters(filters):
    """Add custom filters to the CSV writer filtering register.

    :param filters: A dictionary of filters to register
    """
    global available_filters
    available_filters = dict(list(available_filters.items()) + list(filters.items()))


def prepare_csv_file(path, columns=None, root_path='out'):
    """Erase each csv file and then add column header row.

    :param path: The path to the CSV file
    :param columns: The columns that define the structure of the file (optional)
    :param root_path: The folder root for output file (optional, defaults to out/)
    """
    # By opening the file for writing, we implicitly delete the file contents
    with open(root_path + '/' + path, 'w') as csv_file:
        # Treat file as CSV
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # Write the header
        if columns is not None:
            csv_writer.writerow([c['name'] for c in columns])


def write_records_to_file(path, columns, entities, entity_filter=None, tbl_name=None, root_path='out'):
    """For a list of entity objects, write a record to an output path. This requires that the objects in the entities
    parameter have a 'get_object_set' method that returns a dictionary of objects whose attributes are available.

    :param path: The path to the CSV file
    :param columns: The dictionary of columns for data values to write for each entity
    :param entities: A list of entity objects to write out to the file
    :param entity_filter: An (attribute, value) tuple that will be evaluated against each object in entities to see if
                          that object should be written to the file. If not provided, all entities are written to file.
                          The attribute is expected to be directly on the entity and is not checked (will raise an
                          exception if not present).
    :param tbl_name: Name of table this row is being generated for (optional). This is used to generate unique record
                     ID values that are unique within a given table.
    :param root_path: The folder root for output file (optional, defaults to out/)
    """
    with open(root_path + '/' + path, 'a') as csv_file:
        # Treat file as CSV
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # Write each row
        for entity in entities:
            if entity_filter is None or getattr(entity, entity_filter[0]) == entity_filter[1]:
                row = writers_util.build_csv_row_values(entity.get_object_set(), columns, available_filters, tbl_name)
                csv_writer.writerow(row)
