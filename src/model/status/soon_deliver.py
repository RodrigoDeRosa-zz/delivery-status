from src.model.status.status import Status


class SoonDeliver(Status):

    @classmethod
    def message(cls) -> str:
        return 'Pronto a ser entregado'
