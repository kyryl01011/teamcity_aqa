from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):

    def auth_api(self, user_creds):
        self.session.auth = user_creds
        csrf_token = self.send_request('GET', '/authenticationTest.html?csrf').text
        if not csrf_token:
            raise ValueError('No csrf token received or invalid')
        self._update_session_headers(**{'X-TC-CSRF-Token': csrf_token})