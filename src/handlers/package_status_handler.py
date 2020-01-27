from src.handlers.custom_request_handler import CustomRequestHandler
from src.model.exceptions.business_error import BusinessError
from src.service.status.package_status_request_mapper import PackageStatusRequestMapper
from src.service.status.status_service import StatusService
from src.utils.mapping_utils import MappingUtils


class PackageStatusHandler(CustomRequestHandler):
    """ Handler for package status control. """

    SUPPORTED_METHODS = ['POST', 'GET', 'PATCH']

    async def post(self, package_id):
        try:
            request = PackageStatusRequestMapper.map(self.__parse_body())
            message = await StatusService.set_package_status(request)
            self.make_response({'package': message})
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def get(self, package_id):
        try:
            message = await StatusService.last_known_status(package_id)
            self.make_response({'package': message})
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def patch(self, package_id):
        try:
            request = PackageStatusRequestMapper.map(self.__parse_body())
            message = await StatusService.update_package_status(request)
            self.make_response({'package': message})
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    def __parse_body(self):
        try:
            return MappingUtils.decode_request_body(self.request.body)
        except RuntimeError:
            raise BusinessError(f'Invalid request body {self.request.body}', 400)

    def data_received(self, chunk):
        pass
