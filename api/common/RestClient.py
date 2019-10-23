import logging

import requests

from api.common.RestClientExceptions import ResourceNotFoundException, ResourceUnauthorizedException, \
    ServerIsNotUpException, ResourceErrorException, ResourceRedirectToException
from api.common.Utility import Utility


class RestClient:

    def __init__(self, base_url, component: str):
        self.base_url = base_url
        self.component = component
        self.logger = logging.getLogger(__name__)

    def _get_service_message_response(self, component, curl_return):
        if 'message' in curl_return:
            return curl_return.get('message', f'{component} Error Exception').get('response',
                                                                                  f'{component} Error Exception')
        if 'errors' in curl_return:
            if type(curl_return['errors']) is list or type(curl_return['errors'] is tuple):
                return ' '.join(curl_return['errors'])
            return curl_return.get('errors', f'{component} Error Exception')

        if 'error' in curl_return:
            return curl_return.get('error', f'{component} Error Exception')
        return curl_return

    def http_exception_handling(self, response):
        if response['http_status'] == 404:
            raise ResourceNotFoundException(self.component, response['response'])
        elif response['http_status'] == 401:
            raise ResourceUnauthorizedException(self.component, response['response'])
        elif response['http_status'] == 302:
            raise ResourceRedirectToException(self.component, response['headers']['Location'], response['url'])
        else:
            raise ResourceErrorException(self.component, response['response'])

    def call(self, method, url, headers=None, **kwargs):
        self.logger.info(f"REQUEST TO : {method} {url} {headers}")
        headers = headers
        try:
            self.logger.debug(f'{method} : {self.base_url}{url}')
            resp = requests.request(method, f'{self.base_url}{url}', headers=headers, **kwargs)
            json_response = resp.text

            if Utility.is_json(json_response):
                json_response = resp.json()
            response = {
                'http_status': resp.status_code,
                'response': json_response,
                'headers': resp.headers,
                'url': resp.url
            }
            self.logger.info(f'Response : {response}')
            if resp.status_code != 200:
                self.http_exception_handling(response)
            return response
        except requests.exceptions.ConnectionError:
            raise ServerIsNotUpException(server=f'{self.component} @ {self.base_url}')
        except Exception as e:
            self.logger.error(self)
            self.logger.error(self.base_url + url)
            self.logger.error(str(e), e.args)
            raise e

