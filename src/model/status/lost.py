from src.model.status.status import Status


class Lost(Status):

    @classmethod
    def message(cls) -> str:
        return 'Perdido'
