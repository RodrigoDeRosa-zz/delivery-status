from src.model.package.status.status import Status


class Shipped(Status):

    @classmethod
    def message(cls) -> str:
        return 'En Camino'
