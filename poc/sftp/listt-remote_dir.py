import pysftp
 
srv = pysftp.Connection(host="edwappsrv6.poc.dum.edwdc.net", username="ny_dep", password="nydep123")
 
# Get the directory and file listing
data = srv.listdir()
 
# Closes the connection
srv.close()
 
# Prints out the directories and files, line by line
for i in data:
    print(i)