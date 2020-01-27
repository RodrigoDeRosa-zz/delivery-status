from motor.motor_tornado import MotorClient

from src.utils.logging.logger import Logger


class Mongo:
    """ MongoDB access point. """

    __CLIENT = None
    DB = None

    @classmethod
    def init_async(cls, host='localhost', port=27017, db_name='delivery_status', user=None, password=None):
        """ Create database with asynchronous connector."""
        cls.get_logger().info('Establishing database connection...')
        uri = cls.__create_uri(host, port, user, password)
        # Create db client
        cls.__CLIENT = MotorClient(uri)
        cls.DB = cls.__CLIENT[db_name]

    @classmethod
    def set(cls, db):
        # The received db will always be the same object so concurrence won't be a problem.
        # This is just for a more comfortable usage
        cls.DB = db

    @classmethod
    def get(cls):
        return cls.DB

    @classmethod
    def _drop_database(cls, db_name):
        """ Visible for testing """
        cls.__CLIENT.drop_database(db_name)

    @classmethod
    def __create_uri(cls, host, port, user, password):
        """ Generates database URI"""
        # Create auth string from parameters
        auth = f'{user}:{password}@' if user and password else ''
        # Create database URI
        return f'mongodb://{auth}{host}:{port}'

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)