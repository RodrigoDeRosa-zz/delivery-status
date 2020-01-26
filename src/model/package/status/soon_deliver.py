from src.model.package.status.status import Status


class SoonDeliver(Status):

    @classmethod
    def message(cls) -> str:
        return 'Pronto a ser entregado'
