from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    comparepopulation_view = config.add_view("myedwareproject.controllers.compare_population_criteria.ComparePopulationCriteria",
                                             route_name='comparepopulation')
    config.add_route(name='comparepopulation',
                     pattern='/comparepopulation',
                     view=comparepopulation_view)

    getcomparepopulation_view = config.add_view(view="myedwareproject.controllers.get_compare_population.GetComparePopulation",
                                                route_name='getcomparepopulation')
    config.add_route(name='getcomparepopulation',
                     pattern='/getcomparepopulation',
                     view=getcomparepopulation_view)

#    config.add_route('comparepopulation', '/comparepopulation')
    config.scan()
    return config.make_wsgi_app()
