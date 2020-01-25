from src.status_factory import StatusFactory
from src.status_sorter import StatusSorter


class StatusService:

    @classmethod
    def package_status(cls, notifications: list) -> str:
        # Map notifications to classes
        status_list = [StatusFactory.create(obj) for obj in notifications]
        # Get last status from the list
        return StatusSorter.last_status(status_list).message()
