from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (DBSession, Base,)
import edapi

from edapi import EdApi


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
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
    #routing for class report
    config.add_route('class_report', '/class_report')
    config.scan()
    EdApi(config)
    return config.make_wsgi_app()
