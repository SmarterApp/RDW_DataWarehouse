'''
Created on May 2, 2013

@author: tosako
'''
import subprocess
from pdfmaker.pdf import celery

pdf_procs = ['wkhtmltopdf']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--javascript-delay', '3000']


@celery.task(name='tasks.generate_pdf')
def generate_pdf(cookie, url, outputfile, options=pdf_defaults):
    return subprocess.call(pdf_procs + options + ['--cookie', 'edware', cookie, url, outputfile])
