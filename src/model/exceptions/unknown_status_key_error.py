class UnknownStatusKeyError(RuntimeError):

    def __init__(self, key: str, data: dict):
        self.message = f'Unknown status for key {key} and data {data}.'

    def __str__(self):
        return self.message
