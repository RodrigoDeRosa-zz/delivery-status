from src.model.status.status import Status


class WaitingForWithdrawal(Status):

    @classmethod
    def message(cls) -> str:
        return 'En agencia'
