from src.model.exceptions.business_error import BusinessError
from src.model.package.package_status_request import PackageStatusRequest
from src.service.status.status_sorter import StatusSorter
from src.utils.logging.logger import Logger


class StatusService:

    @classmethod
    def package_status(cls, package_status: PackageStatusRequest) -> str:
        cls.get_logger().info(f'Calculating last status for package {package_status.package_id}.')
        # TODO -> Access database to store or update package's last known status
        # Get last status from the list
        last_status = StatusSorter.last_status(package_status.status_list)
        if not last_status: raise BusinessError('No valid status found on list.')
        return last_status.message()

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
