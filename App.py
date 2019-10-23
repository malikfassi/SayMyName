import logging

from flask import make_response, jsonify
from flask_cors import CORS

from api.EncryptedConfiguration.EncryptedConfiguration import EncryptedConfiguration
from api.common.CommonException import CommonException
from api.common.Database import Database
from api.common.Logging import Logging
from api.common.configuration.Config import Flask
from api.common.configuration.ConfigService import ConfigService
from api.common.models.BaseModel import database_proxy


class App(Flask):

    def __init__(self):
        super().__init__(__name__)

        Logging.set_config()
        logging.getLogger('flask_cors').level = logging.DEBUG

        #CONFIGURATION
        self.config.from_yaml('configuration/conf.yaml')
        self.config_service = ConfigService()
        self.config_service.initialize(self.config)
        self.config_service.info()

        CORS(self, resources={r"/api/*": {"origins": "*"}})

        #ROUTE REGISTRATION
        self.register_routes()

        self.db = self.init_db()
        self.create_tables()

        @self.errorhandler(Exception)
        def exception(e):
            if isinstance(e, CommonException):
                message = e.serialize()
            else:
                message = str(e)
            return make_response(jsonify({'error': message}), 400)

        @self.after_request
        def post_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Origin, X-Ledger-Auth, X-Requested-With')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response

    def init_db(self):
        # DB initialization
        db = Database(self.config['DATABASE'])
        database_proxy.initialize(db.db_instance)
        return db

    def create_tables(self):
        self.db.db_instance.create_tables([EncryptedConfiguration], safe=True)

    def register_routes(self):
        # Routes registration
        from api.common.RoutesRegistrar import RoutesRegistrar
        route_registrar = RoutesRegistrar(self)
        route_registrar.register()
