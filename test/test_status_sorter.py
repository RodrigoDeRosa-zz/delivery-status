import unittest

from parameterized import parameterized

from src.model.status.status import Status
from src.model.status.delivered import Delivered
from src.model.status.handling import Handling
from src.model.status.lost import Lost
from src.model.status.manufacturing import Manufacturing
from src.model.status.printed import Printed
from src.model.status.ready_to_print import ReadyToPrint
from src.model.status.shipped import Shipped
from src.model.status.soon_deliver import SoonDeliver
from src.model.status.stolen import Stolen
from src.model.status.waiting_for_withdrawal import WaitingForWithdrawal
from src.status_sorter import StatusSorter


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
