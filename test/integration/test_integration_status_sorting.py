import unittest

from src.model.exceptions.invalid_status_data_error import InvalidStatusDataError
from src.model.exceptions.unknown_status_key_error import UnknownStatusKeyError
from src.model.status.delivered import Delivered
from src.model.status.stolen import Stolen
from src.status_service import StatusService


class TestIntegrationStatusSorting(unittest.TestCase):

    def test_full_flow_ok(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'handling', 'substatus': 'manufacturing'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'shipped', 'substatus': 'soon deliver'},
            {'status': 'shipped', 'substatus': 'waiting for withdrawal'},
            {'status': 'delivered'}
        ]
        self.__do_test(notifications, Delivered.message())

    def test_missing_steps(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'shipped', 'substatus': 'waiting for withdrawal'},
            {'status': 'delivered'}
        ]
        self.__do_test(notifications, Delivered.message())

    def test_stolen(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'handling', 'substatus': 'manufacturing'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        self.__do_test(notifications, Stolen.message())

    def test_invalid_notifications_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'substatus': 'manufacturing'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        with self.assertRaises(InvalidStatusDataError):
            self.__do_test(notifications, Stolen.message())

    def test_unknown_state_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'returned to office'}
        ]
        with self.assertRaises(UnknownStatusKeyError):
            self.__do_test(notifications, Stolen.message())

    def __do_test(self, notifications, expected_result):
        self.assertEqual(expected_result, StatusService.package_status(notifications))


if __name__ == '__main__':
    unittest.main()
