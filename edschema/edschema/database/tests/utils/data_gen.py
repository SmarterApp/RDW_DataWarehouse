'''
Created on Feb 14, 2013

@author: agrebneva
'''
import os
from random import choice, randrange
import shutil
import uuid
import datetime
from edschema.database.connector import IDbUtil
from zope import component
import csv

# Some sample data to generate convincing records
__sample_data = {
    "first_name": ["Takashi", "Adam", "Doris", "David", "Nidhi", "Nitesh", "Seth", "Lili", "Drew", "Ken", "Anna"],
    "last_name": ["Osako", "Oren", "Ip", "Wu", "Paroha", "Sanhkalkar", "Wimberly", "Chen", "Brien", "Allen", "Grebneva"],
    "middle_name": ["", "J", "L"],
    "state_code": ["NC"],
    "from_date": ["2012-12-01"],
    "to_date": ["9999-12-01"],
    "district_id": ["d1", "d2"],
    "district_name": ["Daybreak", "Sunset"],
    "school_id": ["sc1", "sc2"],
    "section_id": ["sec1", "sec2"],
    "grade": range(0, 12),
    "gender": ["M", "F", "N/A"],
    "hier_user_type": ['Teacher', 'Staff']
}

__counter = 0


# Get resource dir
def get_resource_dir():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, '..', 'resources'))


# helper to call generate data with csv funciton
def generate_cvs_templates(datasource_name=''):
    templ_resources = os.path.join(get_resource_dir(), 'tmpl')
    if os.path.exists(templ_resources):
        shutil.rmtree(templ_resources)
    os.makedirs(templ_resources)

    generate_data(write_to_csv, datasource_name=datasource_name)


# generate data for each found table and execute table_data_func for each set of rows
def generate_data(table_data_func, datasource_name=''):
    metadata = component.queryUtility(IDbUtil, datasource_name).get_metadata()
    for table in metadata.sorted_tables:
        rows = []
        for _ in range(5):
            rows.append(get_row_values(table.columns))
        table_data_func(table, rows)


#  write sample rows to csv
def write_to_csv(table, rows):
    templ_resources = os.path.join(get_resource_dir(), 'tmpl')
    file = os.path.join(templ_resources, table.name + '.csv')
    if os.path.exists(file):
        os.remove(file)
    with open(file, mode='w') as file_obj:
            writer = csv.DictWriter(file_obj, table.columns._data.keys())
            writer.writeheader()
            for i in range(len(rows)):
                writer.writerow(rows[i])


#  generate values for columns of a row
def get_row_values(cols):
    def col_map(col):
        return (col.name, infer_value(col))
    return dict(map(col_map, cols))


#  get sample values from a provided dictionary
def try_from_sample(name):
    #  endswith function
    def f(key):
        return name.endswith(key)
    sub = list(filter(f, __sample_data.keys()))
    if sub is None or len(sub) == 0:
        return None
    else:
        return choice(__sample_data[sub[0]])


#  generate value for a column
def infer_value(col):
    global __counter
    v = try_from_sample(col.name)
    if v is not None:
        return v
    datatype = col.type.python_type
    if datatype in [int, float, complex]:
        return randrange(0, 1000)
    elif datatype == str:
        if col.name.endswith("_id") or col.name == "id":
            return str(uuid.uuid4())
        __counter += 1
        return col.name.replace('_', ' ').title() + " " + str(__counter)
    elif datatype is datetime:
        return "01/01/2011"
    elif datatype == bool:
        return 1
