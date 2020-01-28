import types
import unittest

from parameterized import parameterized
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from src.database.mongo import Mongo
from src.handlers.package_status_handler import PackageStatusHandler
from src.model.package.package_status import PackageStatus
from src.utils.logging.logger import Logger
from src.utils.mapping_utils import MappingUtils
from test.test_utils.mock_logger import MockLogger


class TestIntegrationPackageStatus(AsyncHTTPTestCase):

    def setUp(self) -> None:
        super(TestIntegrationPackageStatus, self).setUp()
        setattr(Logger,
                MockLogger.build_logger.__name__,
                types.MethodType(MockLogger.build_logger, Logger))

    def tearDown(self) -> None:
        super(TestIntegrationPackageStatus, self).tearDown()
        # This is ugly but kind of the only way to test the asynchronous database access
        Mongo._drop_database('test_database')

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
        self.__do_test('/packages', 'POST', request_body, {'package': PackageStatus.Delivered.message()})

    def test_missing_steps(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'shipped', 'substatus': 'waiting for withdrawal'},
            {'status': 'delivered'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test('/packages', 'POST', request_body, {'package': PackageStatus.Delivered.message()})

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
        self.__do_test('/packages', 'POST', request_body, {'package': PackageStatus.Stolen.message()})

    def test_invalid_notifications_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'substatus': 'manufacturing'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test('/packages', 'POST', request_body, expected_code=400, error_extract='Invalid')

    def test_unknown_state_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'returned to office'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.__do_test('/packages', 'POST', request_body, expected_code=400, error_extract='Unknown')

    @parameterized.expand([
        [{'id': '', 'inputs': [{'status': 'handling'}]}, 'ID field'],
        [{'inputs': [{'status': 'handling'}]}, 'ID field'],
        [{'id': 'id', 'inputs': []}, 'Inputs'],
        [{'id': 'id'}, 'Inputs']
    ])
    def test_invalid_request_body(self, request_body, error_extract):
        self.__do_test('/packages', 'POST', request_body, expected_code=400, error_extract=error_extract)

    def test_store_and_check(self):
        self.__do_test('/packages', 'POST', {'id': 'id', 'inputs': [{'status': 'delivered'}]})
        self.__do_test('/packages/id', 'GET', expected_body={'package': 'Entregado'})

    def test_get_unknown_package(self):
        self.__do_test('/packages/id', 'GET', expected_code=400, error_extract='No package found')

    def test_store_and_update(self):
        self.__do_test('/packages', 'POST', {'id': 'id', 'inputs': [{'status': 'handling'}]})
        self.__do_test('/packages', 'PATCH', {'id': 'id', 'inputs': [{'status': 'delivered'}]},
                       expected_body={'package': 'Entregado'})

    def test_update_non_existent_package(self):
        self.__do_test('/packages', 'PATCH', {'id': 'id', 'inputs': [{'status': 'shipped'}]},
                       expected_body={'package': 'En Camino'})

    def __do_test(self, path, method, request_body=None, expected_body=None, expected_code=200, error_extract=None):
        response = self.fetch(path, method=method, body=None if not request_body else str(request_body))
        self.assertEqual(expected_code, response.code)
        body = MappingUtils.decode_request_body(response.body)
        if error_extract: self.assertTrue(error_extract in body['message'])
        if expected_body: self.assertEqual(expected_body, body)

    def get_app(self):
        app = Application([('/packages/?(?P<package_id>[^/]+)?', PackageStatusHandler)])
        # This is ugly but kind of the only way to test the asynchronous database access
        Mongo.init(db_name='test_database')
        app.settings['db'] = Mongo.get()
        return app


if __name__ == '__main__':
    unittest.main()
