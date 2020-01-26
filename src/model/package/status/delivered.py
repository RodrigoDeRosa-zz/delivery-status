from src.model.package.status.status import Status


class Delivered(Status):

    @classmethod
    def message(cls) -> str:
        return 'Entregado'
