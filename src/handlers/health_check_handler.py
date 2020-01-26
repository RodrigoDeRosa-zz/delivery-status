from src.handlers.custom_request_handler import CustomRequestHandler


class HealthCheckHandler(CustomRequestHandler):
    """ Handler for health checks. """

    SUPPORTED_METHODS = ['GET']

    def get(self):
        self.make_response('OK')

    def _log(self):
        # Avoid logging request data on health checks
        pass
