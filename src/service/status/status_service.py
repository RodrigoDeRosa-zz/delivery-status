from src.model.package.package_status_request import PackageStatusRequest
from src.service.status.status_sorter import StatusSorter
from src.utils.logging.logger import Logger


class StatusService:

    @classmethod
    def package_status(cls, package_status: PackageStatusRequest) -> str:
        cls.get_logger().info(f'Calculating last status for package {package_status.package_id}.')
        # TODO -> Access database to store or update package's last known status
        # Get last status from the list
        return StatusSorter.last_status(package_status.status_list).message()

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
