import unittest

from parameterized import parameterized

from src.model.package.package_status import PackageStatus
from src.utils.mapping_utils import MappingUtils
from test.integration.integration_test_case import IntegrationTestCase


class TestIntegrationPackageStatus(IntegrationTestCase):

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
        self.do_test('/packages', 'POST', request_body, {'package': PackageStatus.Delivered.message()})

    def test_missing_steps(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'printed'},
            {'status': 'shipped'},
            {'status': 'shipped', 'substatus': 'waiting for withdrawal'},
            {'status': 'delivered'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.do_test('/packages', 'POST', request_body, {'package': PackageStatus.Delivered.message()})

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
        self.do_test('/packages', 'POST', request_body, {'package': PackageStatus.Stolen.message()})

    def test_invalid_notifications_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'substatus': 'manufacturing'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'stolen'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.do_test('/packages', 'POST', request_body, expected_code=400, error_extract='Invalid')

    def test_unknown_state_raises_exception(self):
        notifications = [
            {'status': 'handling'},
            {'status': 'ready to ship', 'substatus': 'ready to print'},
            {'status': 'shipped'},
            {'status': 'not delivered', 'substatus': 'returned to office'}
        ]
        request_body = {'id': 'id', 'inputs': notifications}
        self.do_test('/packages', 'POST', request_body, expected_code=400, error_extract='Unknown')

    @parameterized.expand([
        [{'id': '', 'inputs': [{'status': 'handling'}]}, 'ID field'],
        [{'inputs': [{'status': 'handling'}]}, 'ID field'],
        [{'id': 'id', 'inputs': []}, 'Inputs'],
        [{'id': 'id'}, 'Inputs']
    ])
    def test_invalid_request_body(self, request_body, error_extract):
        self.do_test('/packages', 'POST', request_body, expected_code=400, error_extract=error_extract)

    def test_store_and_check(self):
        self.do_test('/packages', 'POST', {'id': 'id', 'inputs': [{'status': 'delivered'}]})
        self.do_test('/packages/id', 'GET', expected_body={'package': 'Entregado'})

    def test_get_unknown_package(self):
        self.do_test('/packages/id', 'GET', expected_code=400, error_extract='No package found')

    def test_store_and_update(self):
        self.do_test('/packages', 'POST', {'id': 'id', 'inputs': [{'status': 'handling'}]})
        self.do_test('/packages', 'PATCH', {'id': 'id', 'inputs': [{'status': 'delivered'}]},
                     expected_body={'package': 'Entregado'})

    def test_update_non_existent_package(self):
        self.do_test('/packages', 'PATCH', {'id': 'id', 'inputs': [{'status': 'shipped'}]},
                     expected_body={'package': 'En Camino'})


if __name__ == '__main__':
    unittest.main()
