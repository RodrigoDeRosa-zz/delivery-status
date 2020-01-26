from src.model.package.status.status import Status


class Stolen(Status):

    @classmethod
    def message(cls) -> str:
        return 'Robado'
