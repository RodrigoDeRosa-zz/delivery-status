import unittest
from unittest import mock

from src.database.package_dao import PackageDAO
from src.model.exceptions.business_error import BusinessError
from src.model.package.package_status import PackageStatus
from src.model.package.package_status_request import PackageStatusRequest
from src.service.status.status_service import StatusService
from src.service.status.status_sorter import StatusSorter


class TestStatusService(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.exists_foo = PackageDAO.exists
        PackageDAO.exists = self.__exists_mock_coroutine
        self.store_foo = PackageDAO.store
        PackageDAO.store = self.__store_mock_coroutine
        self.find_foo = PackageDAO.find
        PackageDAO.find = self.__find_mock_coroutine

    def tearDown(self) -> None:
        PackageDAO.exists = self.exists_foo
        PackageDAO.store = self.store_foo
        PackageDAO.find = self.find_foo

    @mock.patch.object(StatusSorter, 'last_status', return_value=PackageStatus.Handling)
    async def test_flow_ok(self, sorter_mock):
        self.exists_result = False
        request = PackageStatusRequest('id', [PackageStatus.Handling])
        self.assertEqual(PackageStatus.Handling.message(), await StatusService.set_package_status(request))
        self.assertEqual(1, sorter_mock.call_count)
        self.assertEqual([PackageStatus.Handling], sorter_mock.call_args[0][0])

    @mock.patch.object(StatusSorter, 'last_status', return_value=None)
    async def test_no_status_found_raises_exception(self, sorter_mock):
        self.exists_result = False
        request = PackageStatusRequest('id', [PackageStatus.Handling])
        with self.assertRaises(BusinessError) as context:
            await StatusService.set_package_status(request)
        self.assertEqual('No valid status found on list.', context.exception.message)
        self.assertEqual(1, sorter_mock.call_count)
        self.assertEqual([PackageStatus.Handling], sorter_mock.call_args[0][0])

    @mock.patch.object(StatusSorter, 'last_status', return_value=None)
    async def test_existing_package_raises_exception(self, sorter_mock):
        self.exists_result = True
        request = PackageStatusRequest('id', [PackageStatus.Handling])
        with self.assertRaises(BusinessError) as context:
            await StatusService.set_package_status(request)
        self.assertTrue('Package with id' in context.exception.message)
        self.assertEqual(0, sorter_mock.call_count)

    async def __exists_mock_coroutine(self, package_id):
        """ This is needed to mock coroutines """
        return self.exists_result

    async def __find_mock_coroutine(self, package_id):
        """ This is needed to mock coroutines """
        return self.find_result

    async def __store_mock_coroutine(self, package_id, status):
        """ This is needed to mock coroutines """
        pass


if __name__ == '__main__':
    unittest.main()
