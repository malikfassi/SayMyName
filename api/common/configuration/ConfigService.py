import logging

from api.common.configuration.ConfigExceptions import ConfigDoesNotExistException
from api.common.singleton import singleton


@singleton
class ConfigService:
    def __init__(self):
        self.config = None
        self.logger = logging.getLogger()

    def get(self, *args):
        try:
            value = self.config
            if value is None:
                return None
            for attr in args:
                value = value[attr]
            return value
        except KeyError:
            raise ConfigDoesNotExistException

    def initialize(self, config):
        self.config = config

    def info(self):
        if self.config['ENVIRONMENT'] == 'development':
            self.logger.info('****************************************************')
            self.logger.info(f'Initializing gate with the following configuration : ')
            self.logger.info(f'PORT = {self.get("PORT")}')
            self.logger.info(f'HOST = {self.get("HOST")}')
            self.logger.info(f'AUTH_TOKEN_HEADER_NAME = {self.get("AUTH_TOKEN_HEADER_NAME")}')
            self.logger.info('****************************************************')
