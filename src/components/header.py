import allure

from src.actions.page_actions import PageActions


class Header:
    def __init__(self, actions: PageActions):
        self.actions = actions
        self.user_avatar_selector = '[data-test="avatar"]'
        self.projects_selector = '[data-test-title="Projects"]'

    def check_login(self):
        with allure.step('Check if user avatar is visible on page to prove it\'s logged in'):
            self.actions.wait_selector(self.user_avatar_selector)
            # self.actions.assert_selector_visible(self.user_avatar_selector)

    def go_to_projects_page(self):
        with allure.step('Click project selector from header to go to projects page'):
            self.actions.click_selector(self.projects_selector)