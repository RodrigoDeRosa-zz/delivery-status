import unittest

from src.database.package_dao import PackageDAO
from src.model.package.package_status import PackageStatus
from src.service.statistics.statistics_service import StatisticsService


class TestStatisticsService(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        super(TestStatisticsService, self).setUp()
        self.count = PackageDAO.count

    def tearDown(self) -> None:
        super(TestStatisticsService, self).tearDown()
        PackageDAO.count = self.count

    async def test_statistics_calculation(self):
        PackageDAO.count = self.__mock_count
        result = await StatisticsService.packages_statistics()
        self.assertEqual(0, result['packages_count'])
        for key, value in result['count_by_category'].items():
            self.assertTrue(key in dir(PackageStatus))
            self.assertEqual(0, value)

    async def __mock_count(self, status=None):
        return 0


if __name__ == '__main__':
    unittest.main()
