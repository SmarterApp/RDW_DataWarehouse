# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on May 20, 2013

@author: dip
'''


class ServicesError(Exception):
    '''
    a general EdApi error.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg


class PdfGenerationError(ServicesError):
    '''
    a custom exception raised when a pdf generation failed
    '''
    def __init__(self, msg='Pdf Generation failed'):
        self.msg = msg


class PDFUniteError(PdfGenerationError):
    '''
    a custom exception raised when a pdfunite is failed
    '''
    def __init__(self, msg='pdfunite is failed'):
        self.msg = msg
