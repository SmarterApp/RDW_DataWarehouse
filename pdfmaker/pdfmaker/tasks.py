'''
Created on May 2, 2013

@author: tosako
'''
import subprocess
from pdfmaker.pdf import celery


@celery.task
def generate_pdf(cookie, url, outputfile):
    return subprocess.call(['wkhtmltopdf', '--grayscale', '--page-size', 'Letter', '--enable-javascript', '--javascript-delay', '10000', '--cookie', 'edware', cookie, url, outputfile])
