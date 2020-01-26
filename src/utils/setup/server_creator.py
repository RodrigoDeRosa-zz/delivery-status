from tornado.httpserver import HTTPServer


class ServerCreator:

    @classmethod
    def create(cls, app, port) -> HTTPServer:
        server = HTTPServer(app)
        server.bind(port)
        return server
