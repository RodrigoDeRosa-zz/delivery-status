from tornado.web import Application

from src.utils.logging.logger import Logger
from src.utils.setup.router import Router


class AppCreator:

    @staticmethod
    def create_app():
        """ Create Tornado application. """
        Logger('AppCreator').info('Creating Tornado Application...')
        return Application(Router.get_routes())
