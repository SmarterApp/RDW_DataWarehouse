'''
Created on Oct 10, 2013

@author: bpatel
'''
import pysftp
import sys
import os

# Defines the name of the file for download

remote_file = sys.argv[1]

srv = pysftp.Connection(host="edwappsrv6.poc.dum.edwdc.net", username="ny_dep",
                            password="nydep123")

# Download the file from the remote server

srv.get(remote_file, './downloaded.pdf')

# Closes the connection
srv.close()

# To Run this script python pickup_file.py 'pickup/SBAC_CollaborationSurvey_43929585.pdf'
