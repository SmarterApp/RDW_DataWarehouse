'''
Created on Oct 10, 2013

@author: bpatel
'''
import pysftp
import sys
import os

# Defines the name of the file for upload

local_file = sys.argv[1]

srv = pysftp.Connection(host="edwappsrv6.poc.dum.edwdc.net", username="ny_arr",
                            password="nyarr123")

# To upload the file

srv.put(local_file, 'filedrop/' + os.path.basename(local_file))

# Closes the connection
srv.close()

#To drop a file run python dnld_upld_file.py 'path of the file'
