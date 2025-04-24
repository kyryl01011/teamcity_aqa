from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.auth_api()

    def auth_api(self):
        self.session.auth = ('admin', 'admin')
        csrf_token = self.send_request('GET', '/authenticationTest.html?csrf').text
        if not csrf_token:
            raise ValueError('No csrf token received or invalid')
        self._update_session_headers(**{'X-TC-CSRF-Token': csrf_token})