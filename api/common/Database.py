import logging

import sys
from peewee import OperationalError, PostgresqlDatabase


class Database:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db_instance = self.load_database()
        try:
            self.db_instance.connect()
        except OperationalError as e:
            print(e)
            self.logger.error(
                f"Please make sur your {self.config['ENGINE']} server is up or check the configuration file (configuration/vault_conf.yaml)"
            )
            sys.exit()

    def load_database(self):
        self.logger.info(f"DB use - {self.config['ENGINE']}")
        if self.config["ENGINE"] == "PostgreSQL":
            return PostgresqlDatabase(
                self.config["SCHEMA"],
                user=self.config["USER"],
                password=self.config["PASSWORD"],
                host=self.config["HOST"],
                port=self.config["PORT"],
            )

    def connect_db(self):
        if self.db_instance.is_closed():
            self.db_instance.connect()

    def close_db(self):
        if not self.db_instance.is_closed():
            self.db_instance.close()
