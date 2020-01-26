class UnknownStatusKeyError(RuntimeError):

    def __init__(self, data: dict):
        self.message = f'Unknown status for data {data}.'

    def __str__(self):
        return self.message
