import requests
from enums.hosts import BASE_URL

class CustomRequester:
    base_headers = dict({'Content-Type': 'application/json', 'Accept': 'application/json'})

    def __init__(self):
        self.base_url = BASE_URL

    def send_request(self, method, endpoint, data=None, expected_status=200):
        url = self.base_url + endpoint
        response = self.session.request(method, url, json=data)
        if response.status_code != expected_status:
            raise ValueError(f'Unexpected status code: {response.status_code}')
        return response
    
    def _update_session_headers(self, **kwargs):
        self.headers = self.base_headers.copy()
        self.headers.update(**kwargs)
        self.session.headers.update(self.headers)