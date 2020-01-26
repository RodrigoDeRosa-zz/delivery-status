from typing import List, Type

from src.model.package.status.status import Status


class PackageStatusRequest:

    def __init__(self, package_id: str, status_list: List[Type[Status]]):
        self.package_id = package_id
        self.status_list = status_list
