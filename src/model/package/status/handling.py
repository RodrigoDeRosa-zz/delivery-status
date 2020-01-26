from src.model.package.status.status import Status


class Handling(Status):

    @classmethod
    def message(cls) -> str:
        return 'Le notificamos al vendedor sobre tu compra'
