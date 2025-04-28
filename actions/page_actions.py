import allure
from playwright.sync_api import Page, expect


class PageActions:
    def __init__(self, page: Page):
        self.page = page

    def pause_page(self):
        with allure.step('Pause the page'):
            self.page.pause()

    def go_to_url(self, endpoint):
        with allure.step(f'Load url: {endpoint}'):
            self.page.goto(endpoint)

    def click_selector(self, selector):
        with allure.step(f'Click selector: "{selector}"'):
            self.page.click(selector)

    def wait_selector(self, selector):
        with allure.step(f'Wait for selector: "{selector}"'):
            self.page.wait_for_selector(selector)

    def wait_page_load(self):
        with allure.step(f'Wait page to load: "{self.page.url}"'):
            self.page.wait_for_load_state('load')

    def fill_selector_with_text(self, selector, text):
        with allure.step(f'Fill selector: "{selector}" with text: "{text}"'):
            self.page.fill(selector, text)

    def type_selector_with_text(self, selector, text):
        with allure.step(f'Type selector: "{selector}" with text: "{text}"'):
            self.page.type(selector, text)

    def assert_selector_contains_text(self, selector, text):
        with allure.step(f'Check if selector "{selector}" contains text: "{text}"'):
            expect(self.page.locator(selector)).to_contain_text(text)

    def assert_selector_visible(self, selector):
        with allure.step(f'Check if selector "{selector}" is visible on page'):
            expect(self.page.locator(selector)).to_be_visible()