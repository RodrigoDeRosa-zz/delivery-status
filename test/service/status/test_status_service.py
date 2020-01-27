import unittest
from unittest import mock

from src.model.exceptions.business_error import BusinessError
from src.model.package.package_status import PackageStatus
from src.model.package.package_status_request import PackageStatusRequest
from src.service.status.status_service import StatusService
from src.service.status.status_sorter import StatusSorter


class TestStatusService(unittest.TestCase):

    @mock.patch.object(StatusSorter, 'last_status', return_value=PackageStatus.Handling)
    def test_flow_ok(self, sorter_mock):
        request = PackageStatusRequest('id', [PackageStatus.Handling])
        self.assertEqual(PackageStatus.Handling.message(), StatusService.package_status(request))
        self.assertEqual(1, sorter_mock.call_count)
        self.assertEqual([PackageStatus.Handling], sorter_mock.call_args[0][0])

    @mock.patch.object(StatusSorter, 'last_status', return_value=None)
    def test_no_status_found_raises_exception(self, sorter_mock):
        request = PackageStatusRequest('id', [PackageStatus.Handling])
        with self.assertRaises(BusinessError) as context:
            StatusService.package_status(request)
        self.assertEqual('No valid status found on list.', context.exception.message)


if __name__ == '__main__':
    unittest.main()
