from api.common.CommonException import CommonException


class AuthTokenIsMissingException(CommonException):
    def __init__(self):
        super().__init__()
        self.message = 'Auth Token is missing'
        self.code = 105


class ChallengeInvalidOrExpiredException(CommonException):
    def __init__(self):
        super().__init__()
        self.message = 'Challenge invalid or expired'
        self.code = 101