class Status:

    def __init__(self, message):
        self.__message = message

    def message(self):
        return self.__message if self.__message else None
