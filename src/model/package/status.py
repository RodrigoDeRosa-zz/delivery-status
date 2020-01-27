class Status:

    def __init__(self, message, name):
        self.__message = message
        self.__name = name

    def message(self):
        return self.__message

    def name(self):
        return self.__name
