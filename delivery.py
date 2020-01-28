from tornado.ioloop import IOLoop

from src.database.mongo import Mongo
from src.utils.logging.logger import Logger
from src.utils.parsing_utils import ParsingUtils
from src.utils.setup.app_creator import AppCreator
from src.utils.setup.server_creator import ServerCreator


def start():
    # Parse command line arguments
    port, processes, db_data, logging_data = ParsingUtils.parse_arguments()
    # Set up logger
    Logger.set_up(**logging_data)
    # Create Tornado application
    Logger(__name__).info('Setting up application...')
    app = AppCreator.create_app()
    # Start server on given port and with given processes
    ServerCreator.create(app, port).start(processes)
    # Establish database connection for each process
    Mongo.init(**db_data)
    Mongo.create_indexes()
    app.settings['db'] = Mongo.get()
    # Start event loop
    Logger(__name__).info(f'Listening on http://localhost:{port}.')
    IOLoop.current().start()


if __name__ == '__main__':
    start()
