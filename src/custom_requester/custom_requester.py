import os

import allure
from src.enums.hosts import BASE_URL
import logging

class CustomRequester:
    base_headers = dict({'Content-Type': 'application/json', 'Accept': 'application/json'})

    def __init__(self, session):
        self.session = session
        self.base_url = BASE_URL
        self.logger = logging.getLogger(__name__)

    def send_request(self, method, endpoint, json=None, data=None, expected_status=200, need_logging=True):
        with allure.step(f'Sending {method} request to {self.base_url + endpoint} with body: {json}{data}, expected_status: {expected_status}'):
            url = self.base_url + endpoint
            response = self.session.request(method, url, json=json, data=data)
            if need_logging:
                self.log_request_and_response(response)
            if response.status_code != expected_status:
                raise ValueError(f'Unexpected status code: {response.status_code}')
            return response
    
    def _update_session_headers(self, **kwargs):
        with allure.step(f'Updating session headers: {kwargs}'):
            self.headers = self.base_headers.copy()
            self.headers.update(**kwargs)
            self.session.headers.update(self.headers)

    def log_request_and_response(self, response):
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = '\\\n'.join([f'-H {header}:{value}' for header, value in request.headers.items()])
            full_test_name = f'pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}'
            body = ''
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
            body = f"-d '{body}' \n" if body != '{}' else ''
            self.logger.info(
                f'{GREEN}{full_test_name}{RESET}\n'
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )
            response_status = response.status_code
            is_success = response.ok
            response_data = response.text

            if not is_success:
                self.logger.info(
                    f"\tRESPOSE:"
                    f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                    f"\nDATA: {RED}{response_data}{RESET}"
                )
        except Exception as e:
            self.logger.info(f'\nLogging went wrong: {type({e})} - {e}')
