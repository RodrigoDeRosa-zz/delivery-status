class InvalidStatusDataError(RuntimeError):

    def __init__(self, data: dict):
        self.message = f'Invalid data object. {data}'

    def __str__(self):
        return self.message
