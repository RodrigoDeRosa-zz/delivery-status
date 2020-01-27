import unittest

from parameterized import parameterized

from src.model.exceptions.invalid_status_data_error import InvalidStatusDataError
from src.model.exceptions.unknown_status_key_error import UnknownStatusKeyError

from src.model.package.package_status import PackageStatus
from src.service.status.status_factory import StatusFactory


class TestStatusFactory(unittest.TestCase):

    @parameterized.expand(
        [
            ['handling', None, PackageStatus.Handling],
            ['Handling', None, PackageStatus.Handling],
            ['HANDLING', None, PackageStatus.Handling],
            ['handling', 'manufacturing', PackageStatus.Manufacturing],
            ['handling', 'Manufacturing', PackageStatus.Manufacturing],
            ['handling', 'MANUFACTURING', PackageStatus.Manufacturing],
            ['ready to ship', 'ready to print', PackageStatus.ReadyToPrint],
            ['ready to ship', 'Ready To Print', PackageStatus.ReadyToPrint],
            ['ready to ship', 'Ready to print', PackageStatus.ReadyToPrint],
            ['READY TO SHIP', 'READY TO PRINT', PackageStatus.ReadyToPrint],
            ['ready to ship', 'printed', PackageStatus.Printed],
            ['shipped', None, PackageStatus.Shipped],
            ['shipped', 'soon deliver', PackageStatus.SoonDeliver],
            # I wouldn't call this a bug. It has no sense to check these cases
            ['shipped', 'soon_deliver', PackageStatus.SoonDeliver],
            ['shipped', 'waiting for withdrawal', PackageStatus.WaitingForWithdrawal],
            ['delivered', None, PackageStatus.Delivered],
            ['not delivered', 'stolen', PackageStatus.Stolen],
            ['not delivered', 'lost', PackageStatus.Lost],
        ]
    )
    def test_mapping_ok(self, status, sub_status, expected_class):
        test_data = {'status': status, 'substatus': sub_status}
        result_class = StatusFactory.create(test_data)
        assert expected_class == result_class

    @parameterized.expand(
        [
            [None, None, InvalidStatusDataError],
            [None, 'sub_status', InvalidStatusDataError],
            ['unknown', None, UnknownStatusKeyError],
            ['handling', 'unknown', UnknownStatusKeyError]
        ]
    )
    def test_invalid_status_data_raises_exception(self, status, sub_status, expected_error):
        test_data = {'status': status, 'substatus': sub_status}
        with self.assertRaises(expected_error):
            StatusFactory.create(test_data)


if __name__ == '__main__':
    unittest.main()
