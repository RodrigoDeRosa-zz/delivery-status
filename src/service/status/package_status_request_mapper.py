from src.model.exceptions.business_error import BusinessError
from src.model.exceptions.invalid_status_data_error import InvalidStatusDataError
from src.model.exceptions.unknown_status_key_error import UnknownStatusKeyError
from src.model.package.package_status_request import PackageStatusRequest
from src.service.status.status_factory import StatusFactory
from src.utils.mapping_utils import MappingUtils


class PackageStatusRequestMapper:

    @classmethod
    def map(cls, request_body: bytes) -> PackageStatusRequest:
        try:
            request_body = MappingUtils.decode_request_body(request_body)
        except RuntimeError:
            raise BusinessError(f'Invalid request body {request_body}', 400)
        # Check request body elements
        if not request_body.get('id'):
            raise BusinessError('Failed to map incoming request. CAUSE: ID field should not be null or empty.', 400)
        if not request_body.get('inputs'):
            raise BusinessError('Failed to map incoming request. CAUSE: Inputs list should not be null or empty.', 400)
        # Map request body
        package_id = request_body.get('id')
        # Map status to model classes
        try:
            status_list = [StatusFactory.create(status_data) for status_data in request_body.get('inputs', {})]
        except (InvalidStatusDataError, UnknownStatusKeyError) as e:
            raise BusinessError(f'Failed to map incoming request. CAUSE: {e}', 400)
        # Create DTO with mapped data
        return PackageStatusRequest(package_id, status_list)
