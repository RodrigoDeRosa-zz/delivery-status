import unittest
from unittest import mock

from src.model.package.package_status_request import PackageStatusRequest
from src.model.package.status.handling import Handling
from src.service.status.status_service import StatusService
from src.service.status.status_sorter import StatusSorter


class TestStatusService(unittest.TestCase):

    @mock.patch.object(StatusSorter, 'last_status', return_value=Handling)
    def test_flow_ok(self, sorter_mock):
        request = PackageStatusRequest('id', [Handling])
        self.assertEqual(Handling.message(), StatusService.package_status(request))
        self.assertEqual(1, sorter_mock.call_count)
        self.assertEqual([Handling], sorter_mock.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
