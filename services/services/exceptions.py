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
