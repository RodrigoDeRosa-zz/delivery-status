from tornado.ioloop import IOLoop

from src.utils.logging.logger import Logger
from src.utils.setup.app_creator import AppCreator
from src.utils.setup.server_creator import ServerCreator


def start():
    port = 5000
    processes = 1
    Logger.set_up()
    # Create Tornado application
    Logger(__name__).info('Setting up application...')
    app = AppCreator.create_app()
    # Start server on given port and with given processes
    ServerCreator.create(app, port).start(processes)
    Logger(__name__).info(f'Listening on http://localhost:{port}.')
    # Start event loop
    IOLoop.current().start()


if __name__ == '__main__':
    start()
