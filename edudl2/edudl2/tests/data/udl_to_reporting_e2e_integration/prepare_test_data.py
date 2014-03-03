'''
Created on Mar 1, 2014

@author: nparoha
'''
import gnupg
import os
import zipfile
import time
import csv
import fnmatch
import re


SOURCE_PATH = ""
DESTI_PATH = ''


# get the gpg file names
jsonfiles = []
for file in os.listdir("/Users/nparoha/Desktop/temp/shall_02-28-2014_12-39-27"):
    if fnmatch.fnmatch(file, '*.json'):
        jsonfiles.append(str(file.rpartition('METADATA_')[2][:-5]))

