from flask import g
from peewee import DoesNotExist

from api.common.Utility import Utility


class CommonException(Exception):
    def __init__(self):
        self.message = 'error'
        self.code = 0
        self.name = Utility.get_type_name(self.__class__.__name__)

    def serialize(self):
        serialized_exception = {
            'code': self.code,
            'message': self.message,
            'name': self.name,
        }
        return serialized_exception


class BadFormatException(CommonException):
    def __init__(self):
        super().__init__()
        self.message = 'BadFormat'
        self.code = 1012


class CommonDoesNotExist(CommonException, DoesNotExist):
    def __init__(self, object_name, *query, **filters):
        super().__init__()
        self.message = f'{object_name} does not exist'