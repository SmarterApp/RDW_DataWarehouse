
'''
Created on Sep 25, 2013

@author: dip
'''
import csv
import io


class CSVRenderer(object):
    '''
    A CSV Renderer for returning csv content in response
    '''

    def __init__(self, info):
        pass

    def __call__(self, value, system):
        with io.StringIO() as out_stream:
            writer = csv.writer(out_stream, delimiter=',', quoting=csv.QUOTE_NONE)

            writer.writerow(value['header'])
            writer.writerows(value['rows'])

            response = system['request'].response
            response.content_type = 'text/csv'
            response.headers['Content-Disposition'] = ("attachment; filename=\"%s\"" % value['file_name'])
            content = out_stream.getvalue()
        return content
