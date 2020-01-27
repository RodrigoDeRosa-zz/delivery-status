from typing import List

from src.database.package_dao import PackageDAO
from src.model.exceptions.business_error import BusinessError
from src.model.package.package_status_request import PackageStatusRequest
from src.model.package.status import Status
from src.service.status.status_sorter import StatusSorter
from src.utils.logging.logger import Logger


class StatusService:

    @classmethod
    async def last_known_status(cls, package_id: str) -> str:
        cls.get_logger().info(f'Retrieving package with id {package_id}.')
        last_known_status = await cls.__retrieve_status(package_id)
        if not last_known_status: raise BusinessError(f'No package found with id {package_id}', 400)
        return last_known_status.message()

    @classmethod
    async def set_package_status(cls, package_status_request: PackageStatusRequest) -> str:
        # Check if the given package has already been posted
        if await PackageDAO.exists(package_status_request.package_id):
            raise BusinessError(f'Package with id {package_status_request.package_id} already exists.', 400)
        # Find last status and return
        return await cls.__analyze_and_store(package_status_request.package_id, package_status_request.status_list)

    @classmethod
    async def update_package_status(cls, package_status_request: PackageStatusRequest) -> str:
        # Get last known status for the given package (if existent)
        last_known_status = await cls.__retrieve_status(package_status_request.package_id)
        # Append last known status to given list of status
        package_status_request.status_list.append(last_known_status)
        # Find last status and return
        return await cls.__analyze_and_store(package_status_request.package_id, package_status_request.status_list)

    @classmethod
    async def __analyze_and_store(cls, package_id: str, status_list: List[Status]) -> str:
        # Get last status from the list
        cls.get_logger().info(f'Calculating last status for package {package_id}.')
        last_status = StatusSorter.last_status(status_list)
        if not last_status: raise BusinessError('No valid status found on list.')
        # Store new 'last status' for the given package
        await PackageDAO.store(package_id, last_status.name())
        # Return last status' message
        return last_status.message()

    @classmethod
    async def __retrieve_status(cls, package_id: str) -> Status:
        return await PackageDAO.find(package_id)

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
