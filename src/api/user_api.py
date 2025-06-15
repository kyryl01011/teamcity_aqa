

from http import HTTPStatus

import allure

from src.custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):

    def create_user(self, user_data):
        with allure.step(f'Create user with data: {user_data}'):
            return self.send_request('POST', '/app/rest/users', json=user_data)
    
    def delete_user(self, user_locator):
        with allure.step(f'Delete user with locator: {user_locator}'):
            return self.send_request('DELETE', f'/app/rest/users/{user_locator}', expected_status=HTTPStatus.NO_CONTENT)