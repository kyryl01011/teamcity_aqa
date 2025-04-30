import allure

from entities.user import User
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/login.html'
        self.username_input_selector = 'input#username'
        self.password_input_selector = 'input#password'
        self.login_button_selector = 'input[name="submitLogin"]'

    def go_to_login_page(self):
        with allure.step(f'Go to login page with url: {self._get_url(self._endpoint)}'):
            self.actions.go_to_url(self._get_url(self._endpoint))
            self.actions.wait_page_load()

    def fill_login_from(self, username, password):
        with allure.step(f'Fill login form with username: "{username}" and password: "{password}"'):
            self.actions.fill_selector_with_text(self.username_input_selector, username)
            self.actions.fill_selector_with_text(self.password_input_selector, password)

    def log_in(self):
        with allure.step(f'Click login button with selector: {self.login_button_selector}'):
            self.actions.click_selector(self.login_button_selector)
