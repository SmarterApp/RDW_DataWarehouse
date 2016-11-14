'''
Created on Jan 5, 2013

@author: swimberly
'''

import os.path

from nameinfo import NameInfo
from StatisticalDataGeneration.src import gennames


def read_name_files():
    '''
    Read a file of name statistics of the form:
    "NAME    FREQUENCY CUM_FREQ    RANK"
    Return three 1,000,000 length arrays of male, female and last names
    generated based on the statistics associated with each name.
    '''

    try:
        basepath = os.path.dirname(__file__)
        malefilename = os.path.abspath(os.path.join(basepath, '..', 'datafiles', 'name_lists', 'dist.male.first'))
        femalefilename = os.path.abspath(os.path.join(basepath, '..', 'datafiles', 'name_lists', 'dist.female.first'))
        lastfilename = os.path.abspath(os.path.join(basepath, '..', 'datafiles', 'name_lists', 'dist.all.last'))

        mfile = open(malefilename, 'r')
        male_names = _load_names(mfile)
        mfile.close()

        ffile = open(femalefilename, 'r')
        female_names = _load_names(ffile)
        ffile.close()

        lfile = open(lastfilename, 'r')
        last_names = _load_names(lfile)
        lfile.close()

        mdict, fdict, ldict = gennames.generate_all_names(male_names, female_names, last_names)

        return gennames.name_dict_to_list(mdict), gennames.name_dict_to_list(fdict), gennames.name_dict_to_list(ldict)

    except:
        print("Error while reading file")
        return False, False, False


def _load_names(fileobject):
    '''
    Private Method
    Take the lines of an open file and loop through each pulling
    out the data to create NameInfo objects
    return a list of NameInfo objects
    '''

    lines = fileobject.readlines()

    names = []
    for line in lines:
        name_list = line.split()
        names.append(NameInfo(name_list[0], float(name_list[1]),
                              float(name_list[2]), int(name_list[3])))

    return names


class PeopleNames(object):
    '''
    Singleton Class
    Instance variables:
    male_names -- list of 1,000,000 male names appearing based on frequency
    female_names -- list of 1,000,000 female names appearing based on frequency
    last_names -- list of 1,000,000 last names appearing based on frequency
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PeopleNames, cls).__new__(cls, *args, **kwargs)

            male_list, female_list, last_list = read_name_files()

            cls._instance.male_names = male_list
            cls._instance.female_names = female_list
            cls._instance.last_names = last_list
        return cls._instance
