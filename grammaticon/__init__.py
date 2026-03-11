from functools import partial

from pyramid.config import Configurator

from clld.web.app import menu_item

# we must make sure custom models are known at database initialization!
from grammaticon import models  # noqa
from grammaticon.interfaces import IConcept, IFeature


_ = lambda s: s  # noqa
_("Parameter")
_("Parameters")
_("Contribution")
_("Contributions")
_("Contributor")
_("Contributors")
_("Sentence")
_("Sentences")
_("Value Set")
_("Value Sets")
_("Value")
_("Values")
_("Address")
_("Datapoint")
_("Datapoints")


def main(_global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.register_resource('concept', models.Concept, IConcept, with_index=True)
    config.register_resource('feature', models.Feature, IFeature, with_index=True)
    config.add_page('conceptrelations')

    config.register_menu(
        ('concepts', partial(menu_item, 'concepts')),
        ('features', partial(menu_item, 'features')),
        ('contributions', partial(menu_item, 'contributions')),
        ('sources', partial(menu_item, 'sources')),
        ('conceptrelations', lambda _ctx, req: (req.route_url('conceptrelations'), 'Concept relations')),
    )

    config.add_route('relations', '/relations')
    return config.make_wsgi_app()
