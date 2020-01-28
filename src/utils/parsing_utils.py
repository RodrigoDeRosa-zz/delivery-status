from argparse import ArgumentParser


class ParsingUtils:

    @classmethod
    def parse_arguments(cls):
        """ Get environment from program arguments. tornado.options could be used instead of ArgumentParser. """
        parser = ArgumentParser()
        # Set up argument values
        parser.add_argument('--proc', nargs='?', default=1, type=int, help='Number of processes. 0 is one per CPU.')
        parser.add_argument('--port', nargs='?', default=5000, type=int, help='Port where application will listen.')
        parser.add_argument('--db_host', nargs='?', default='localhost', help='MongoDB host.')
        parser.add_argument('--db_port', nargs='?', default=27017, type=int, help='MongoDB port.')
        parser.add_argument('--db_name', nargs='?', default='delivery_status', help='MongoDB database name.')
        parser.add_argument('--db_user', nargs='?', default=None, help='MongoDB authentication user.')
        parser.add_argument('--db_password', nargs='?', default=None, help='MongoDB authentication password.')
        parser.add_argument('--log_host', nargs='?', default=None, help='UDP logging server hostname.')
        parser.add_argument('--log_port', nargs='?', default=None, type=int, help='UDP logging server port.')
        # Get program arguments
        args = parser.parse_args()
        # Create DB data dictionary
        db_data = dict()
        db_data['host'] = args.db_host
        db_data['port'] = args.db_port
        db_data['db_name'] = args.db_name
        db_data['user'] = args.db_user
        db_data['password'] = args.db_password
        # UDP logging parameters
        logging_data = {'log_host': args.log_host, 'log_port': args.log_port}
        return args.port, args.proc, db_data, logging_data
