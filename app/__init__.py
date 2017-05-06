from pyramid.config import Configurator

import logging
log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('models')
    config.include('.routes')
    config.scan()
    # Celery config file (developer.ini) or create celery.ini ?
    config.configure_celery(global_config['__file__'])
    return config.make_wsgi_app()
