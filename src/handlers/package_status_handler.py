from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.exceptions.business_error import BusinessError
from src.service.status.package_status_request_mapper import PackageStatusRequestMapper
from src.service.status.status_service import StatusService
from src.utils.mapping_utils import MappingUtils


class PackageStatusHandler(CustomRequestHandler):
    """ Handler for package status control. """

    SUPPORTED_METHODS = ['POST']  # ['GET', 'POST', 'PATCH']

    def post(self):
        try:
            request = PackageStatusRequestMapper.map(self.__parse_body())
            message = StatusService.package_status(request)
            self.make_response({'package': message})
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    # TODO -> Get last status for a given package
    # async def get(self):
    #    pass

    # TODO -> Update package's last status
    # async def patch(self):
    #    pass

    def __parse_body(self):
        try:
            return MappingUtils.decode_request_body(self.request.body)
        except RuntimeError:
            raise BusinessError(f'Invalid request body {self.request.body}', 400)

    def data_received(self, chunk):
        pass
