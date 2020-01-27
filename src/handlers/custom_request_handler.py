from tornado.web import RequestHandler

from src.database.mongo import Mongo


class CustomRequestHandler(RequestHandler):

    INTERNAL_ERROR_MESSAGE = 'Internal Server Error. ' \
                             'Our best engineers were [probably] notified and are [probably] running to fix it.'

    def prepare(self):
        Mongo.set(self.settings['db'])

    def data_received(self, chunk):
        pass

    def make_error_response(self, status_code, message):
        """ Create a common error response. """
        self.set_status(status_code)
        response = {'status': status_code, 'message': message}
        self.write(response)

    def make_response(self, response, status_code=200):
        """ Create a common success response. """
        self.set_status(status_code)
        self.write(response)

