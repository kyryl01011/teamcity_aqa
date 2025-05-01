

import allure
from pages.base_page import BasePage

class FirstSetupFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/mnt'

class DataBaseSetupFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/mnt'
        self.database_connection_page_selector = 'h1:has-text("Database connection setup")'

    def wait_database_connection_setup_page(self):
        with allure.step(f'Wait for database connection setup page by selector: {self.database_connection_page_selector}'):
            self.actions.wait_selector(self.database_connection_page_selector)

class LicenseAgreementFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/showAgreement.html'
        self.license_agreement_checkbox_selector = 'div.license-agreement-checkbox-wrapper > label[for="accept"]:has-text("Accept license agreement")'
        self.license_agreement_continue_button_selector = 'div.continueBlock > input[name="Continue"]'

    def wait_license_agreement_page(self):
        with allure.step(f'Wait for license agreement page by selector: {self.license_agreement_checkbox_selector}'):
            self.actions.wait_selector(self.license_agreement_checkbox_selector, 300000)

    def proceed_license_agreement_page(self):
        with allure.step(f'Click agreement checkbox with selector: {self.license_agreement_checkbox_selector}'):
            self.actions.click_selector(self.license_agreement_checkbox_selector)
            self.actions.click_selector(self.license_agreement_continue_button_selector)

class UserRegistrationFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/mnt'
        self.username_input_selector = 'input#input_teamcityUsername'
        self.password_input_selector = 'input#password1'
        self.confirm_password_input_selector = 'input#retypedPassword'
        self.submit_registration_button_selector = 'input.loginButton[value="Create Account"]'

    def wait_for_registration_page(self):
        with allure.step(f'Wait registration page by selector: {self.username_input_selector}'):
            self.actions.wait_selector(self.username_input_selector)

    def fill_registration_form(self, username='admin', password='admin'):
        with allure.step(f'Fill registration for with username: "{username}" and password: "{password}"'):
            self.actions.fill_selector_with_text(self.username_input_selector, username)
            self.actions.fill_selector_with_text(self.password_input_selector, password)
            self.actions.fill_selector_with_text(self.confirm_password_input_selector, password)
            self.actions.click_selector(self.submit_registration_button_selector)

class SetupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/mnt'
        self.first_setup = FirstSetupFragment(page)
        self.database_setup = DataBaseSetupFragment(page)
        self.license_agreement = LicenseAgreementFragment(page)
        self.user_registration = UserRegistrationFragment(page)
        self.initializing_server_span_selector = 'span#stageDescription:has-text("Initializing TeamCity server components")'
        self.proceed_button_selector = 'input#proceedButton'


    def go_to_setup_page(self):
        with allure.step(f'Load teamcity first setup page with url: {self._get_url(self._endpoint)}'):
            self.actions.go_to_url(self._get_url(self._endpoint))

    def click_proceed_button(self):
        with allure.step(f'Click proceed button on setup page with selector: {self.proceed_button_selector}'):
            self.actions.click_selector(self.proceed_button_selector)

    def set_up(self, username='admin', password='admin'):
        with allure.step('Proceed all setup pages'):
            self.actions.go_to_url(self._get_url(self._endpoint))
            self.actions.click_selector(self.proceed_button_selector)
            self.database_setup.wait_database_connection_setup_page()
            self.actions.click_selector(self.proceed_button_selector)
            self.license_agreement.wait_license_agreement_page()
            self.license_agreement.proceed_license_agreement_page()
            self.user_registration.wait_for_registration_page()
            self.user_registration.fill_registration_form(username, password)
            self.header.check_login()
