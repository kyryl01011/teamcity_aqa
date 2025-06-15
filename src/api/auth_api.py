import allure

from src.custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):

    def auth_and_get_csrf_token(self, user_creds):
        with allure.step(f'Auth user with creds: "{user_creds}" and get csrf token'):
            self.session.auth = user_creds
            csrf_token = self.send_request('GET', '/authenticationTest.html?csrf').text
            if not csrf_token:
                raise ValueError('No csrf token received or invalid')
            self._update_session_headers(**{'X-TC-CSRF-Token': csrf_token})