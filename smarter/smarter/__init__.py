from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.path import caller_package, caller_module, package_of
import sys
import edapi
import os
from database import connector


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    connector.engine = engine_from_config(settings, 'sqlalchemy.', pool_size=20, max_overflow=0)

    config = Configurator(settings=settings)

    # include add routes from edapi. Calls includeme
    config.include(edapi)

    if not os.path.lexists(os.getcwd() + '/assets'):
        os.symlink('../assets', os.getcwd() + '/assets')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('assets', '../assets', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('checkstatus', '/status')
    #
    config.add_route('comparing_populations', '/comparing_populations')
    config.add_route('test1', '/test1')
    config.add_route('template', '/template')
    config.add_route('generateComparePopulations', '/comPopResults')
    config.add_route('inputComparePopulations', '/comPop')
    config.add_route('generateComparePopulationsAl', '/comPopResultsAl')
    config.add_route('inputComparePopulationsAl', '/comPopAl')
    config.add_route('datatojson2', '/datatojson2')
    config.add_route('inputdata2', '/inputdata2')
    # splita's code
    config.add_route('comparepopulation', '/comparepopulation')
    config.add_route('getcomparepopulation', '/getcomparepopulation')

    # routing for individual student report
    config.add_route('indiv_student', '/indiv_student_report')
    #r routing for *bootstrapped* individual student report
    config.add_route('indiv_student_bootstrap', '/indiv_student_report_bootstrap')
    #routing for class report
    config.add_route('class_report', '/class_report')
    config.add_route('student_report', '/student_report')

    # scans smarter
    config.scan()

    return config.make_wsgi_app()
