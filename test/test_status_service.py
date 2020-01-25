import unittest
from unittest import mock
from unittest.mock import call

from src.model.status.handling import Handling
from src.status_factory import StatusFactory
from src.status_service import StatusService
from src.status_sorter import StatusSorter


class TestStatusService(unittest.TestCase):

    @mock.patch.object(StatusFactory, 'create', return_value=Handling)
    @mock.patch.object(StatusSorter, 'last_status', return_value=Handling)
    def test_flow_ok(self, sorter_mock, factory_mock):
        notifications = [
            {'status': 'handling'},
            {'status': 'handling', 'substatus': 'manufacturing'},
            {'status': 'delivered'}
        ]
        self.assertEqual(Handling.message(), StatusService.package_status(notifications))
        self.assertEqual(3, factory_mock.call_count)
        self.assertEqual(1, sorter_mock.call_count)
        self.assertEqual(call({'status': 'handling'}), factory_mock.call_args_list[0])
        self.assertEqual(call({'status': 'handling', 'substatus': 'manufacturing'}), factory_mock.call_args_list[1])
        self.assertEqual(call({'status': 'delivered'}), factory_mock.call_args_list[2])
        self.assertEqual([Handling, Handling, Handling], sorter_mock.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
