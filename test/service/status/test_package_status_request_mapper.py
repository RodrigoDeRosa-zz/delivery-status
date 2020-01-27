import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from src.model.exceptions.business_error import BusinessError
from src.model.exceptions.invalid_status_data_error import InvalidStatusDataError
from src.model.package.package_status import PackageStatus
from src.service.status.package_status_request_mapper import PackageStatusRequestMapper
from src.service.status.status_factory import StatusFactory


class TestPackageStatusRequestMapper(unittest.TestCase):

    def setUp(self) -> None:
        self.create = StatusFactory.create

    def tearDown(self) -> None:
        StatusFactory.create = self.create

    @parameterized.expand(
        [
            [[{'status': 'handling'}]],
            [[{'status': 'handling'}, {'status': 'delivered'}, {'status': 'shipped'}]],
        ]
    )
    def test_map_ok(self, inputs):
        # Prepare mock
        StatusFactory.create = MagicMock(name='create')
        StatusFactory.create.return_value = PackageStatus.Handling
        # Do test
        request_body = {'id': 'some_id', 'inputs': inputs}
        result = PackageStatusRequestMapper.map(request_body)
        self.assertEqual('some_id', result.package_id)
        self.assertEqual(PackageStatus.Handling, result.status_list[0])
        self.assertEqual(len(inputs), len(result.status_list))
        self.assertEqual(len(inputs), StatusFactory.create.call_count)

    @parameterized.expand(
        [
            [{'id': '', 'inputs': []}, 'ID field'],
            [{'inputs': []}, 'ID field'],
            [{'id': 'some_id', 'inputs': []}, 'Inputs list'],
            [{'id': 'some_id'}, 'Inputs list']
        ]
    )
    def test_invalid_request_body_raises_exception(self, request_body, message_extract):
        with self.assertRaises(BusinessError) as context:
            PackageStatusRequestMapper.map(request_body)
        self.assertTrue(message_extract in context.exception.message)

    def test_mapping_exception_raises_business_error(self):
        # Prepare mock
        StatusFactory.create = MagicMock(name='create')
        StatusFactory.create.side_effect = InvalidStatusDataError({'data': 'test'})
        # Do test
        request_body = {'id': 'test_id', 'inputs': [{'status': 'handling'}]}
        with self.assertRaises(BusinessError) as context:
            PackageStatusRequestMapper.map(request_body)
        self.assertTrue('Invalid data object' in context.exception.message)


if __name__ == '__main__':
    unittest.main()
