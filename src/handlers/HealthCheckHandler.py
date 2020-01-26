from tornado.web import RequestHandler


class HealthCheckHandler(RequestHandler):
    """ Handler for health checks. """

    SUPPORTED_METHODS = ['GET']

    def get(self):
        self.write('OK')

    def _log(self):
        # Avoid logging request data on health checks
        pass

    def data_received(self, chunk):
        pass
