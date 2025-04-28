from entities.user import User
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/login.html'
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Log in")

    def go_to_login_page(self):
        self.actions.go_to_url(self._get_url(self._endpoint))
        self.actions.wait_page_load()

    def fill_login_from(self, username, password):
        self.actions.fill_selector_with_text(self.username_input, username)
        self.actions.fill_selector_with_text(self.password_input, password)

    def log_in(self):
        self.actions.click_selector(self.login_button)
