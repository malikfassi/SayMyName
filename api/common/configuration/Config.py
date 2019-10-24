import os
import yaml

from flask import Flask as BaseFlask, Config as BaseConfig


class Config(BaseConfig):
    global_configuration_env_prefix = 'ISO9001'
    global_configuration = [
        'HOST',
        'PORT',
    ]
    databases_allowed = [
        'PostgreSQL'
    ]
    sql_configuration_env_prefix = 'ISO9001'
    sql_configuration = [
        'HOST',
        'PORT',
        'USER',
        'SCHEMA',
        'PASSWORD'
    ]

    """Flask config enhanced with a `from_yaml` method."""
    def verify_conf_parameters_are_set(self):
        # verify global configuration
        for config_param in Config.global_configuration:
            if config_param not in self:
                raise ConfigParameterException(config_param)

        # verify database configuration
        if 'DATABASE' not in self:
            raise ConfigParameterException('DATABASE')
        if 'ENGINE' not in self['DATABASE']:
            raise ConfigParameterException('DATABASE ENGINE')
        if self['DATABASE']['ENGINE'] not in Config.databases_allowed:
            raise ConfigParameterException(f'Database type {self["DATABASE"]["ENGINE"]} is not allowed. It must be set between {Config.databases_allowed}')
        if self['DATABASE']['ENGINE'] == 'PostgreSQL':
            for db_param in Config.sql_configuration:
                if db_param not in self['DATABASE']:
                    raise ConfigParameterException(f"{self['DATABASE']['ENGINE']} {db_param}")

    def get_envvar(self, path):
        env_var = os.environ.get(path)
        if env_var is not None and env_var.isdigit():
            return int(env_var)
        else:
            return env_var

    def load_and_replace_by_env_variables(self):
        for config_param in Config.global_configuration:
            env_var = self.get_envvar(f'{Config.global_configuration_env_prefix}{config_param}')
            if env_var is not None:  # replace conf variable by env variable
                self[config_param] = env_var

        if self['DATABASE']['ENGINE'] == 'PostgreSQL':
            for config_param in Config.sql_configuration:
                env_var = self.get_envvar(f'{Config.sql_configuration_env_prefix}{config_param}')
                if env_var is not None:
                    self['DATABASE'][config_param] = env_var

    def from_yaml(self, config_file):
        env = os.environ.get('FLASK_ENV', 'DEVELOPMENT')
        self['ENVIRONMENT'] = env.lower()
        with open(config_file) as f:
            c = yaml.load(f)
        c = c.get(env, c)
        for key in c.keys():
            if key.isupper():
                self[key] = c[key]
        self.load_and_replace_by_env_variables()
        self.verify_conf_parameters_are_set()
        return self


class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class"""

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)


class ConfigParameterException(Exception):
    def __init__(self, message):
        super().__init__(f'Configuration {message} is missing')
