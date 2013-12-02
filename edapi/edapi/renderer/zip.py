
'''
Created on Dec 2, 2013

@author: ejen
'''
#import edextract.utils.file_archiver
from zipfile import ZipFile
from io import BytesIO


class ZipRenderer(object):
    '''
    A Zip Archive Renderer for returning liar csv content in zip format in response
    '''

    def __init__(self, info):
        pass

    def __call__(self, value, system):
        with BytesIO() as out_stream:
            response = system['request'].response

            # we use only zip32, and we have to use mode 'a' for in memoery zip file
            # we pass in a list of files that have names and contents
            with ZipFile(out_stream, 'a') as zipfile:
                for file in value['files']:
                    zipfile.writestr(file['name'], file['content'])

                # we need to grant file permission to be readable and writable for zipped file in in memory case
                for zfile in zipfile.filelist:
                    zfile.create_system = 0

                # also, zipfile has to close in order to have proper checksum
                zipfile.close()

            response.content_type = 'application/zip'
            response.headers['Content-Disposition'] = ("attachment; filename=\"%s\"" % value['zip_name'])
            content = out_stream.getvalue()
        return content
