'''
Created on Jun 17, 2013

@author: dawu
'''
from pdf.pdf_generator import PDFGenerator
import sys
    
# TODO: grabs new results from database/file that need reports generated


# TODO: includes trigger mechanism from UDL process


# test
if __name__ == '__main__':
    #params = {'studentGuid' : '3efe8485-9c16-4381-ab78-692353104cce'}
    #Øsend_pdf_request(params, report='indivStudentReport.html', settings=settings)
    configFile = sys.argv[1]
    PDFGenerator(configFile).start()
