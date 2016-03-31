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
