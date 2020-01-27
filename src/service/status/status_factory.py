from src.model.exceptions.invalid_status_data_error import InvalidStatusDataError
from src.model.exceptions.unknown_status_key_error import UnknownStatusKeyError
from src.model.package.package_status import PackageStatus
from src.model.package.status import Status


class StatusFactory:

    # This is a way of avoiding a big chunk of ifs
    __INSTANCES = {
        'handling': PackageStatus.Handling,
        'handling-manufacturing': PackageStatus.Manufacturing,
        'ready_to_ship-ready_to_print': PackageStatus.ReadyToPrint,
        'ready_to_ship-printed': PackageStatus.Printed,
        'shipped': PackageStatus.Shipped,
        'shipped-soon_deliver': PackageStatus.SoonDeliver,
        'shipped-waiting_for_withdrawal': PackageStatus.WaitingForWithdrawal,
        'delivered': PackageStatus.Delivered,
        'not_delivered-stolen': PackageStatus.Stolen,
        'not_delivered-lost': PackageStatus.Lost
    }

    @classmethod
    def create(cls, data: dict) -> Status:
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
        return cls.__INSTANCES[key]
