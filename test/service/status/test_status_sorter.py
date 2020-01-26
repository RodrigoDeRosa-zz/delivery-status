import unittest

from parameterized import parameterized

from src.model.package.status.status import Status
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
from src.service.status.status_sorter import StatusSorter


class TestStatusSorter(unittest.TestCase):

    @parameterized.expand(
        [
            [[], Status],
            # This simulates a non included status in the sorting
            [[Status], Status],
            [[Handling, Manufacturing, ReadyToPrint, Printed, Shipped, SoonDeliver, WaitingForWithdrawal, Delivered], Delivered],
            [[Handling, Delivered], Delivered],
            [[SoonDeliver, Shipped, Lost, Printed, Delivered], Lost],
            [[SoonDeliver, Delivered, Shipped, Printed], Delivered],
            [[SoonDeliver, Shipped, Printed], SoonDeliver],
            [[Stolen, Delivered], Stolen],
            [[Delivered, Stolen], Delivered],
            [[Lost, Stolen, Delivered], Lost],
        ]
    )
    def test_sorting(self, status_list, expected_result):
        result = StatusSorter.last_status(status_list)
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
