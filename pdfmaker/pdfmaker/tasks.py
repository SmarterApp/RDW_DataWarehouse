'''
Created on May 2, 2013

@author: tosako
'''
from celery import Celery
import subprocess
celery = Celery('pdfmaker', backend='amqp', broker='amqp://guest@localhost//', include=['tasks'])

@celery.task
def generate_pdf(cookie, url, outputfile):
    return subprocess.call(['wkhtmltopdf', '--grayscale', '--page-size', 'Letter', '--enable-javascript', '--javascript-delay', '10000', '--cookie', 'edware', cookie, url, outputfile]);
    
