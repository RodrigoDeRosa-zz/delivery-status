from src.database.package_dao import PackageDAO
from src.model.package.package_status import PackageStatus
from src.utils.logging.logger import Logger


class StatisticsService:

    @classmethod
    async def packages_statistics(cls):
        """ Gather information about the processed packages. """
        cls.get_logger().info('Retrieving server statistics.')
        packages_count = await PackageDAO.count()
        count_by_category = {status: await PackageDAO.count(status=status) for status in PackageStatus().__dir__()}
        return {'packages_count': packages_count, 'count_by_category': count_by_category}

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
