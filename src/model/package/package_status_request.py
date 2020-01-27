from typing import List

from src.model.package.status import Status


class PackageStatusRequest:

    def __init__(self, package_id: str, status_list: List[Status]):
        self.package_id = package_id
        self.status_list = status_list
