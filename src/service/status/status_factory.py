from typing import Type

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
from src.model.package.status.status import Status
from src.model.package.status.stolen import Stolen
from src.model.package.status.waiting_for_withdrawal import WaitingForWithdrawal


class StatusFactory:

    # This is a way of avoiding a big chunk of ifs
    __INSTANCES = {
        'handling': Handling,
        'handling-manufacturing': Manufacturing,
        'ready_to_ship-ready_to_print': ReadyToPrint,
        'ready_to_ship-printed': Printed,
        'shipped': Shipped,
        'shipped-soon_deliver': SoonDeliver,
        'shipped-waiting_for_withdrawal': WaitingForWithdrawal,
        'delivered': Delivered,
        'not_delivered-stolen': Stolen,
        'not_delivered-lost': Lost
    }

    @classmethod
    def create(cls, data: dict) -> Type[Status]:
        # Extract elements from object
        status = data.get('status')
        sub_status = data.get('substatus')
        if not status:
            raise InvalidStatusDataError(data)
        # Transform for comparison
        status = status.lower()
        sub_status = None if not sub_status else sub_status.lower()
        # Do mapping
        status_key = f"{'_'.join(status.split(' '))}"
        sub_status_key = f"-{'_'.join(sub_status.split(' '))}" if sub_status else ''
        key = status_key + sub_status_key
        if key not in cls.__INSTANCES:
            raise UnknownStatusKeyError(data)
        # Default class is abstract Status
        return cls.__INSTANCES.get(key, Status)
