class Status:

    @classmethod
    def message(cls) -> str:
        raise RuntimeError('Invalid status instance.')
