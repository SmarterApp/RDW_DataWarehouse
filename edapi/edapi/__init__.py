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
This package contains all modules and code of the EdAPI framework

'''
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from edapi.utils import ContentTypePredicate
from edapi.reports import add_report_config
from edapi.renderer import csv, zip


def includeme(config):
    '''
    Initializes and registers the application's REST endpoints. It
    is automatically called by a consumer of edapi when it calls
    config.include(edapi).
    '''

    # routing for retrieving list of report names with GET
    config.add_route('list_of_reports', '/data')

    # routing for the GET, POST, OPTIONS verbs
    config.add_route('report_get_option_post', '/data/{name}')

    # routing for public reports
    config.add_route('public_report_get_option_post', '/public_data/{name}')

    # add public report short URL service
    config.add_route('public_report_short_url', '/public/{sid}')

    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)

    config.add_view_predicate('content_type', ContentTypePredicate)

    config.add_renderer('csv', csv.CSVRenderer)

    config.add_renderer('zip', zip.ZipRenderer)

    # scans edapi, ignoring test package
    config.scan(ignore='edapi.test')
