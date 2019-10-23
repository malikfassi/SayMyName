from logging.config import dictConfig

import coloredlogs as coloredlogs
import yaml
import logging
import os


class Logging:
    elk_prefix = 'log_'

    @staticmethod
    def set_config(default_path='configuration/logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
        """Setup logging configuration"""
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                try:
                    config = yaml.safe_load(f.read())
                    coloredlogs.install(level=os.environ.get('LOG_LEVEL', 'INFO'))
                    logging.getLogger().setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
                    # logging.config.dictConfig(config)
                    # logging.getLogger().setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))
                except Exception as e:
                    print(e)
                    print('Error in Logging Configuration. Using default configs')
                    logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
        else:
            logging.basicConfig(level=default_level)
            print('Config file (%s) not found. Basic config used instead.', default_path)

