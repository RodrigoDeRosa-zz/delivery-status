from src.model.package.status.status import Status


class Manufacturing(Status):

    @classmethod
    def message(cls) -> str:
        return 'El vendedor tendrá listo tu producto pronto y comenzará el envío'
