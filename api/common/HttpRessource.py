import logging
from typing import Dict

from flask import jsonify, make_response


class HttpResource:

    logger = logging.getLogger(__name__)

    @staticmethod
    def _create_error(error_code: int, message: Dict):
        http_response = make_response(jsonify(message), error_code)
        return http_response

    @staticmethod
    def bad_request(message={'message': 'Bad Request'}):
        return HttpResource._create_error(400, message)

    @staticmethod
    def forbidden(message={'message': 'Forbidden'}):
        return HttpResource._create_error(403, message)

    @staticmethod
    def internal_error(trace):
        message = {
            'message': 'Internal Error',
            'trace': trace
        }
        return HttpResource._create_error(500, message)

    @staticmethod
    def success(obj: Dict = {'success': True}):
        http_response = make_response(jsonify(obj))
        return http_response
