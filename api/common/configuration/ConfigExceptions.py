from api.common.CommonException import CommonException


class ConfigDoesNotExistException(CommonException):
    def __init__(self):
        super().__init__()
        self.message = 'The config you are getting does not exist.'
        self.code = 10001
