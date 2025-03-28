from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from grammaticon import models  # noqa
from grammaticon.interfaces import IConcept


_ = lambda s: s  # noqa
_('Parameter')
_('Parameters')
_('Value')
_('Values')
_('Contribution')
_('Contributions')


def main(_global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.register_resource('concept', models.Concept, IConcept, with_index=True)
    config.add_route('relations', '/relations')
    return config.make_wsgi_app()
