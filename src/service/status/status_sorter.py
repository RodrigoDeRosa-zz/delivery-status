from typing import List

from src.model.package.package_status import PackageStatus
from src.model.package.status import Status


class StatusSorter:

    # This allows us to keep out of each class the order of events and, also, allows us to have more than one
    # status per level. For example, an already delivered item shouldn't be able to get lost or stolen.
    __STATUS_ORDER = [
        [PackageStatus.Handling],
        [PackageStatus.Manufacturing],
        [PackageStatus.ReadyToPrint],
        [PackageStatus.Printed],
        [PackageStatus.Shipped],
        [PackageStatus.SoonDeliver],
        [PackageStatus.WaitingForWithdrawal],
        [PackageStatus.Delivered, PackageStatus.Lost, PackageStatus.Stolen]
    ]

    @classmethod
    def last_status(cls, status_list: List[Status]) -> Status:
        max_index = -1
        last_status = None
        # Check for every status of the list
        for status in status_list:
            # To which level it belongs to
            for index, level in enumerate(cls.__STATUS_ORDER):
                # And keep the last one
                if status in level and index > max_index:
                    max_index = index
                    last_status = status
                    break
        return last_status
