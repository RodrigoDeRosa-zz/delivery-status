import types

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from src.database.mongo import Mongo
from src.handlers.package_status_handler import PackageStatusHandler
from src.handlers.statistics_handler import StatisticsHandler
from src.utils.logging.logger import Logger
from src.utils.mapping_utils import MappingUtils
from test.test_utils.mock_logger import MockLogger


class IntegrationTestCase(AsyncHTTPTestCase):

    def setUp(self) -> None:
        super(IntegrationTestCase, self).setUp()
        setattr(Logger,
                MockLogger.build_logger.__name__,
                types.MethodType(MockLogger.build_logger, Logger))

    def tearDown(self) -> None:
        super(IntegrationTestCase, self).tearDown()
        # This is ugly but kind of the only way to test the asynchronous database access
        Mongo._drop_database('test_database')

    def do_test(self, path, method, request_body=None, expected_body=None, expected_code=200, error_extract=None):
        response = self.fetch(path, method=method, body=None if not request_body else str(request_body))
        self.assertEqual(expected_code, response.code)
        body = MappingUtils.decode_request_body(response.body)
        if error_extract: self.assertTrue(error_extract in body['message'])
        if expected_body: self.assertEqual(expected_body, body)

    def get_app(self):
        app = Application([
            ('/packages/statistics', StatisticsHandler),
            ('/packages/?(?P<package_id>[^/]+)?', PackageStatusHandler)
        ])
        # This is ugly but kind of the only way to test the asynchronous database access
        Mongo.init(db_name='test_database')
        app.settings['db'] = Mongo.get()
        return app
