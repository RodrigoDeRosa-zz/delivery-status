from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from src.handlers.HealthCheckHandler import HealthCheckHandler


def start():
    app = Application([
        ('/health/health-check', HealthCheckHandler)
    ])
    server = HTTPServer(app)
    server.bind(5000)
    server.start(1)
    IOLoop.current().start()


if __name__ == '__main__':
    start()
