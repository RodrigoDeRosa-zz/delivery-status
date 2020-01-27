import unittest

from parameterized import parameterized

from src.model.package.package_status import PackageStatus
from src.model.package.status import Status
from src.service.status.status_sorter import StatusSorter


class TestStatusSorter(unittest.TestCase):

    @parameterized.expand(
        [
            [[], None],
            # This simulates a non included status in the sorting
            [[Status('')], None],
            [[PackageStatus.Handling, PackageStatus.Manufacturing, PackageStatus.ReadyToPrint, PackageStatus.Printed,
              PackageStatus.Shipped, PackageStatus.SoonDeliver, PackageStatus.WaitingForWithdrawal,
              PackageStatus.Delivered], PackageStatus.Delivered],
            [[PackageStatus.Handling, PackageStatus.Delivered], PackageStatus.Delivered],
            [[PackageStatus.SoonDeliver, PackageStatus.Shipped, PackageStatus.Lost, PackageStatus.Printed,
              PackageStatus.Delivered], PackageStatus.Lost],
            [[PackageStatus.SoonDeliver, PackageStatus.Delivered, PackageStatus.Shipped, PackageStatus.Printed],
             PackageStatus.Delivered],
            [[PackageStatus.SoonDeliver, PackageStatus.Shipped, PackageStatus.Printed], PackageStatus.SoonDeliver],
            [[PackageStatus.Stolen, PackageStatus.Delivered], PackageStatus.Stolen],
            [[PackageStatus.Delivered, PackageStatus.Stolen], PackageStatus.Delivered],
            [[PackageStatus.Lost, PackageStatus.Stolen, PackageStatus.Delivered], PackageStatus.Lost],
        ]
    )
    def test_sorting(self, status_list, expected_result):
        result = StatusSorter.last_status(status_list)
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
