from src.handlers.health_check_handler import HealthCheckHandler
from src.handlers.package_status_handler import PackageStatusHandler


class Router:

    # Dictionary to map route to Tornado RequestHandler subclasses
    ROUTES = {
        '/health/health-check': HealthCheckHandler,
        '/packages/?(?P<package_id>[^/]+)?': PackageStatusHandler
        # TODO -> Add statistics handler
    }

    @classmethod
    def get_routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
