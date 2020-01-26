from typing import List, Type

from src.model.package.status.delivered import Delivered
from src.model.package.status.handling import Handling
from src.model.package.status.lost import Lost
from src.model.package.status.manufacturing import Manufacturing
from src.model.package.status.printed import Printed
from src.model.package.status.ready_to_print import ReadyToPrint
from src.model.package.status.shipped import Shipped
from src.model.package.status.soon_deliver import SoonDeliver
from src.model.package.status.status import Status
from src.model.package.status.stolen import Stolen
from src.model.package.status.waiting_for_withdrawal import WaitingForWithdrawal


class StatusSorter:

    # This allows us to keep out of each class the order of events and, also, allows us to have more than one
    # status per level. For example, an already delivered item shouldn't be able to get lost or stolen.
    __STATUS_ORDER = [
        [Handling],
        [Manufacturing],
        [ReadyToPrint],
        [Printed],
        [Shipped],
        [SoonDeliver],
        [WaitingForWithdrawal],
        [Delivered, Lost, Stolen]
    ]

    @classmethod
    def last_status(cls, status_list: List[Type[Status]]) -> Type[Status]:
        max_index = -1
        last_status = Status
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
