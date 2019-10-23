from api.common.CommonException import CommonException


def get_service_message_response(component, curl_return):
    if 'message' in curl_return:
        return curl_return['message'].get('response',  f'{component} Error Exception')
    if 'errors' in curl_return:
        if type(curl_return['errors']) is list or type(curl_return['errors'] is tuple):
            return ' '.join(curl_return['errors'])
        return curl_return.get('errors', f'{component} Error Exception')
    return curl_return


class ResourceNotFoundException(CommonException):
    def __init__(self, component, error_str=None):
        super().__init__()
        self.component = component
        self.message = f'{component} not found'
        if error_str is not None:
            self.message += ' : ' + get_service_message_response(component, error_str)
        self.code = 1


class ResourceUnauthorizedException(CommonException):
    def __init__(self, component, error_str=None):
        super().__init__()
        self.component = component
        self.message = f'{component} unauthorized response'
        if error_str is not None:
            self.message += ' : ' + get_service_message_response(component, error_str)
        self.code = 2


class ResourceErrorException(CommonException):
    def __init__(self, component, error_str=None):
        super().__init__()
        self.component = component
        self.message = f'{component} error exception'
        if error_str is not None:
            self.message += ' : ' + str(error_str)
        self.code = 3


class ResourceErrorUnknownException(CommonException):
    def __init__(self, component, status_code, error_str=None):
        super().__init__()
        self.component = component
        self.message = f'{component} error'
        if error_str is not None:
            self.message += ' : ' + get_service_message_response(component, error_str)
        self.code = status_code


class ServerIsNotUpException(CommonException):
    def __init__(self, server):
        super().__init__()
        self.message = f'Server ({server}) is not up'
        self.code = 801


class ResourceRedirectToException(CommonException):
    def __init__(self, component, to_url, from_url):
        super().__init__()
        self.message = f'Resource {component} redirected to {to_url} from {from_url}'
        self.code = 802
