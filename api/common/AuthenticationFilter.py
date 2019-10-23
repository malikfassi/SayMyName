from flask import request, make_response

from api.common.AuthenticationException import AuthTokenIsMissingException, ChallengeInvalidOrExpiredException
from api.common.configuration.ConfigService import ConfigService


class AuthenticationFilter:

    def __init__(self):
        self.unfiltered_paths = ["/_health"]
        self.AUTH_TOKEN = ConfigService().get("AUTH_TOKEN")
        self.AUTH_TOKEN_HEADER_NAME = ConfigService().get("AUTH_TOKEN_HEADER_NAME")

    def _verify_token_present(self):
        try:
            return request.headers[self.AUTH_TOKEN_HEADER_NAME]
        except KeyError:
            raise AuthTokenIsMissingException

    def _verify_valid_token(self):
        token = self._verify_token_present()
        if token == self.AUTH_TOKEN:
            pass
        else:
            raise ChallengeInvalidOrExpiredException
        return True

    def filter(self, apply):
        if apply:
            if request.method == 'OPTIONS':
               pass
            # do not filter unfiltered_paths
            elif any([path in request.path for path in self.unfiltered_paths]):
                pass
            else:
                session = self._verify_valid_token()
                return session
        else:
            pass

