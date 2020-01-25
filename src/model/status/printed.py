from src.model.status.status import Status


class Printed(Status):

    @classmethod
    def message(cls) -> str:
        return 'El vendedor debe despachar tu paquete'
