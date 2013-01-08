from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (DBSession, Base,)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('checkstatus','/status')
    #
    config.add_route('comparing_populations', '/comparing_populations')
    config.add_route('test1', '/test1')
    config.add_route('template', '/template')
    config.add_route('generateComparePopulations','/comPopResults')
    config.add_route('inputComparePopulations','/comPop')
    config.add_route('generateComparePopulationsAl','/comPopResultsAl')
    config.add_route('inputComparePopulationsAl','/comPopAl')
    config.add_route('datatojson2', '/datatojson2')
    config.add_route('inputdata2','/inputdata2')
    # splita's code
    comparepopulation_view = config.add_view(view= "smarter.controllers.compare_population_criteria.ComparePopulationCriteria",
                                             route_name = 'comparepopulation')
    config.add_route(name = 'comparepopulation',
                     pattern = '/comparepopulation',
                     view = comparepopulation_view)

    getcomparepopulation_view = config.add_view(view = "smarter.controllers.get_compare_population.GetComparePopulation",
                                                route_name = 'getcomparepopulation')
    config.add_route(name = 'getcomparepopulation',
                     pattern = '/getcomparepopulation',
                     view = getcomparepopulation_view)
    config.scan()
    return config.make_wsgi_app()
