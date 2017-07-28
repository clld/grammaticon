from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from grammaticon import models
from grammaticon.interfaces import IConcept


_ = lambda s: s
_('Parameter')
_('Parameters')
_('Value')
_('Values')
_('Contribution')
_('Contributions')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.register_resource('concept', models.Concept, IConcept, with_index=True)
    return config.make_wsgi_app()
