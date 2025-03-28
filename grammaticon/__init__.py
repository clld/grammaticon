from functools import partial

from pyramid.config import Configurator

from clld.web.app import menu_item

# we must make sure custom models are known at database initialization!
from grammaticon import models  # noqa
from grammaticon.interfaces import IConcept


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

    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('concepts', partial(menu_item, 'concepts')),
        ('values', partial(menu_item, 'values')),
        # ('parameters', partial(menu_item, 'parameters')),
        ('contributions', partial(menu_item, 'contributions')),
    )

    config.add_route('relations', '/relations')
    return config.make_wsgi_app()
