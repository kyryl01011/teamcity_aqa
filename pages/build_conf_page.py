import allure

from pages.base_page import BasePage


class BuildConfPage(BasePage):
    def __init__(self, page, build_id):
        super().__init__(page)
        self.build_id = build_id
        self._endpoint = f'/buildConfiguration/{build_id}'
        self.run_build_button_selector = 'button[data-test="run-build"]'
        self.run_build_status_popup_selector = 'div.ring-message-description a'

    def go_to_build_conf_page(self):
        with allure.step(f'Go to build conf page with url: {self._get_url(self._endpoint)}'):
            self.actions.go_to_url(self._get_url(self._endpoint))

    def click_run_build_button(self):
        with allure.step(f'Click run build button with selector: {self.run_build_button_selector}'):
            self.actions.click_selector(self.run_build_button_selector)

    def go_to_launched_build_url(self):
        with allure.step(f'Go to launched build url from selector: {self.run_build_status_popup_selector}'):
            url_endpoint = self.actions.get_attribute_value_of_selector(self.run_build_status_popup_selector, 'href')
            print(url_endpoint)
            self.actions.go_to_url(self._get_url(url_endpoint))