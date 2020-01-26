import unittest

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from src.handlers.package_status_handler import PackageStatusHandler
from src.model.package.status.delivered import Delivered
from src.model.package.status.stolen import Stolen
from src.utils.mapping_utils import MappingUtils


class TestIntegrationStatusSorting(AsyncHTTPTestCase):

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
        self.__do_test(notifications, {'package': Delivered.message()})

    def test_missing_steps(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'shipped', 'substatus': 'waiting for withdrawal'},
            {'status': 'delivered'}
        ]
        self.__do_test(notifications, {'package': Delivered.message()})

    def test_stolen(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'handling', 'substatus': 'manufacturing'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        self.__do_test(notifications, {'package': Stolen.message()})

    def test_invalid_notifications_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'substatus': 'manufacturing'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        self.__do_test(notifications, expected_code=400)

    def test_unknown_state_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'returned to office'}
        ]
        self.__do_test(notifications, expected_code=400)

    def __do_test(self, notifications, expected_body=None, expected_code=200):
        request_body = {'id': 'id', 'inputs': notifications}
        response = self.fetch('/packages', method='POST', body=str(request_body))
        self.assertEqual(expected_code, response.code)
        if expected_body:
            body = MappingUtils.decode_request_body(response.body)
            self.assertEqual(expected_body, body)

    def get_app(self):
        return Application([('/packages', PackageStatusHandler)])


if __name__ == '__main__':
    unittest.main()
