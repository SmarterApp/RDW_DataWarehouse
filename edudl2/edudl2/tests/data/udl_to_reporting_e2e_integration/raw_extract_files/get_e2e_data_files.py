'''
Created on March 4, 2014

@author: nparoha
'''

import os
from os import listdir, getcwd, rename

for filename in listdir(getcwd()):
    if filename.startswith('METADATA_ASMT_NC_GRADE_'):
        os.rename(filename, filename[23:])
    elif filename.startswith("ASMT_NC_GRADE_"):
        os.rename(filename, filename[14:])
 
for filename in listdir(getcwd()):
    if "SUMMATIVE" in filename:
        old = filename
        new = filename.replace("SUMMATIVE", "SUM")
        os.rename(old, new)
    elif "INTERIM COMPREHENSIVE" in filename:
        old = filename
        new = filename.replace("INTERIM COMPREHENSIVE", "INT")
        os.rename(old, new)
        
for filename in listdir(getcwd()):
    if "_03-04-2014_15-59-24_" in filename:
        old2 = filename
        new2 = filename.replace("_03-04-2014_15-59-24_", "_")
        os.rename(old2, new2)

tar_file_names = []
for file in os.listdir(os.getcwd()):
    if fnmatch.fnmatch(file, '*.csv'):
        ext = file.split('.')[-2]
        tar_file_names.append(str(ext))

for each in tar_file_names:
    command = "tar -cvzf " + "../tar_files/" + each + ".tar.gz --disable-copyfile " + each + ".csv " + each + ".json" 
    os.system(command)