from src.model.status.status import Status


class ReadyToPrint(Status):

    @classmethod
    def message(cls) -> str:
        return 'El vendedor está preparando tu paquete'
