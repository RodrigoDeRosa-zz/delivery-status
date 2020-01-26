import unittest

from parameterized import parameterized

from src.model.exceptions.invalid_status_data_error import InvalidStatusDataError
from src.model.exceptions.unknown_status_key_error import UnknownStatusKeyError
from src.model.package.status.delivered import Delivered
from src.model.package.status.handling import Handling
from src.model.package.status.lost import Lost
from src.model.package.status.manufacturing import Manufacturing
from src.model.package.status.printed import Printed
from src.model.package.status.ready_to_print import ReadyToPrint
from src.model.package.status.shipped import Shipped
from src.model.package.status.soon_deliver import SoonDeliver
from src.model.package.status.stolen import Stolen
from src.model.package.status.waiting_for_withdrawal import WaitingForWithdrawal
from src.service.status.status_factory import StatusFactory


class TestStatusFactory(unittest.TestCase):

    @parameterized.expand(
        [
            ['handling', None, Handling],
            ['Handling', None, Handling],
            ['HANDLING', None, Handling],
            ['handling', 'manufacturing', Manufacturing],
            ['handling', 'Manufacturing', Manufacturing],
            ['handling', 'MANUFACTURING', Manufacturing],
            ['ready to ship', 'ready to print', ReadyToPrint],
            ['ready to ship', 'Ready To Print', ReadyToPrint],
            ['ready to ship', 'Ready to print', ReadyToPrint],
            ['READY TO SHIP', 'READY TO PRINT', ReadyToPrint],
            ['ready to ship', 'printed', Printed],
            ['shipped', None, Shipped],
            ['shipped', 'soon deliver', SoonDeliver],
            # I wouldn't call this a bug. It has no sense to check these cases
            ['shipped', 'soon_deliver', SoonDeliver],
            ['shipped', 'waiting for withdrawal', WaitingForWithdrawal],
            ['delivered', None, Delivered],
            ['not delivered', 'stolen', Stolen],
            ['not delivered', 'lost', Lost],
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
