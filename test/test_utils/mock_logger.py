class MockLogger:

    def __init__(self, class_name):
        self.class_name = class_name

    @staticmethod
    def build_logger(klazz, class_name):
        return MockLogger(class_name)

    def exception(self, message):
        print(f'ERROR - {self.class_name} - {message}')

    def warning(self, message):
        print(f'WARN - {self.class_name} - {message}')

    def info(self, message):
        print(f'INFO - {self.class_name} - {message}')

    def debug(self, message):
        print(f'DEBUG - {self.class_name} - {message}')
