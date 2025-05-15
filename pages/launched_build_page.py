import sys

import allure

from pages.base_page import BasePage
from playwright.sync_api import TimeoutError as PWTimeoutError


class LaunchedBuildPage(BasePage):
    def __init__(self, page, build_id, launch_id):
        super().__init__(page)
        self.launch_id = launch_id
        self.build_id = build_id
        self._endpoint = f'/buildConfiguration/{build_id}/{launch_id}'
        self.build_status_selector = 'span[data-test-icon="ok"]'

    def go_to_launched_build_page(self):
        with allure.step(f'Go to launched build page with url: {self._get_url(self._endpoint)}'):
            self.actions.go_to_url(self._get_url(self._endpoint))

    def wait_for_success(self):
        with allure.step(f'Wait for selector: {self.build_status_selector} to appear'):
            try:
                self.actions.wait_selector(self.build_status_selector, timeout=90000)
            except PWTimeoutError as e:
                sys.stderr.write(self.page.url)
                allure.attach(self.page.screenshot(full_page=True), name='Build run failure', attachment_type=allure.attachment_type.PNG)
                raise e