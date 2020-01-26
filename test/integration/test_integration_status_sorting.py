import unittest

from parameterized import parameterized
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
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test(request_body, {'package': Delivered.message()})

    def test_missing_steps(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'shipped', 'substatus': 'waiting for withdrawal'},
            {'status': 'delivered'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test(request_body, {'package': Delivered.message()})

    def test_stolen(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'handling', 'substatus': 'manufacturing'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test(request_body, {'package': Stolen.message()})

    def test_invalid_notifications_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'substatus': 'manufacturing'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test(request_body, expected_code=400, error_extract='Invalid')

    def test_unknown_state_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'returned to office'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test(request_body, expected_code=400, error_extract='Unknown')

    @parameterized.expand([
        [{'id': '', 'inputs': [{'status': 'handling'}]}, 'ID field'],
        [{'inputs': [{'status': 'handling'}]}, 'ID field'],
        [{'id': 'id', 'inputs': []}, 'Inputs'],
        [{'id': 'id'}, 'Inputs']
    ])
    def test_invalid_request_body(self, request_body, error_extract):
        self.__do_test(request_body, expected_code=400, error_extract=error_extract)

    def __do_test(self, request_body, expected_body=None, expected_code=200, error_extract=None):
        response = self.fetch('/packages', method='POST', body=str(request_body))
        self.assertEqual(expected_code, response.code)
        body = MappingUtils.decode_request_body(response.body)
        if error_extract: self.assertTrue(error_extract in body['message'])
        if expected_body: self.assertEqual(expected_body, body)

    def get_app(self):
        return Application([('/packages', PackageStatusHandler)])


if __name__ == '__main__':
    unittest.main()
