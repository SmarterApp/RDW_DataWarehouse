'''
Scpript to import the generated data into a schema
'''

import os
import re
import shutil
import subprocess
import sys
import tempfile


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def get_input_args():
    '''
    Creates parser for command line args
    RETURNS vars(args) -- A dict of the command line args
    '''
    
    parser = argparse.ArgumentParser(description='Script to load csv files to a db schema')
    parser.add_argument("-s", "--schema", help="set schema name.  required")
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
    parser.add_argument("--host", default="127.0.0.1:5432", help="postgre host default[127.0.0.1:5432]")
    parser.add_argument("-u", "--user", default="edware", help="postgre username default[edware]")
    parser.add_argument("-p", "--passwd", default="edware", help="postgre password default[edware]")
    args = parser.parse_args()

    args = parser.parse_args()
    return vars(args)


def main():
    


if __name__ == '__main__':
    main()
    
#psql -U postgres -h 127.0.0.1 -d edware -c "\copy ed_new_schema.dim_student from /Users/swimberly/projects/edware/fixture_data_generation/DataGeneration/datafiles/csv/dim_student.csv USING DELIMITERS ',' CSV HEADER"
