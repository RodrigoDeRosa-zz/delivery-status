import unittest

from test.integration.integration_test_case import IntegrationTestCase


class TestIntegrationPackageStatus(IntegrationTestCase):

    def test_statistics_with_no_data(self):
        expected_body = {
            'packages_count': 0,
            'count_by_category': {
                'Handling': 0,
                'Manufacturing': 0,
                'ReadyToPrint': 0,
                'Printed': 0,
                'Shipped': 0,
                'SoonDeliver': 0,
                'WaitingForWithdrawal': 0,
                'Delivered': 0,
                'Lost': 0,
                'Stolen': 0
            }
        }
        self.do_test('/packages/statistics', 'GET', expected_body=expected_body)

    def test_statistics_with_packages(self):
        request_body = {'id': 'id1', 'inputs': [{'status': 'handling'}]}
        self.do_test('/packages', 'POST', request_body)
        request_body = {'id': 'id2', 'inputs': [{'status': 'delivered'}]}
        self.do_test('/packages', 'POST', request_body)
        expected_body = {
            'packages_count': 2,
            'count_by_category': {
                'Handling': 1,
                'Manufacturing': 0,
                'ReadyToPrint': 0,
                'Printed': 0,
                'Shipped': 0,
                'SoonDeliver': 0,
                'WaitingForWithdrawal': 0,
                'Delivered': 1,
                'Lost': 0,
                'Stolen': 0
            }
        }
        self.do_test('/packages/statistics', 'GET', expected_body=expected_body)


if __name__ == '__main__':
    unittest.main()
