from src.handlers.custom_request_handler import CustomRequestHandler
from src.service.statistics.statistics_service import StatisticsService


class StatisticsHandler(CustomRequestHandler):

    async def get(self):
        """ Returns statistical data from the server. """
        try:
            response = await StatisticsService.packages_statistics()
            self.make_response(response)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
