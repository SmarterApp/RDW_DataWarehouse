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
Created on Jul 4, 2014

@author: tosako
'''


class ServicesConstants():
    COVER_SHEET_NAME_PREFIX = 'cover_sheet_grade_'
    # minimum cover file size of pdf generated
    MINIMUM_COVER_FILE_SIZE = 200
    PAGECOUNT = 'pageCount'
    MAX_PDFUNITE_FILE = 50
    PDF_MERGE_MAX_RETRY = 10
    PDF_MERGE_RETRY_DELAY = 120
