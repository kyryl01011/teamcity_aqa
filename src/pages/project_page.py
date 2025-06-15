import allure

from src.pages.base_page import BasePage


class ProjectPage(BasePage):
    def __init__(self, page, proj_id):
        super().__init__(page)
        self.proj_id = proj_id
        self._endpoint = f'/admin/editProject.html?projectId={proj_id}'
        self.create_build_conf_selector = 'span:has-text("Create build configuration")'

    def click_create_build_conf_button(self):
        with allure.step(f'Click create build conf button with selector: {self.create_build_conf_selector}'):
            self.actions.click_selector(self.create_build_conf_selector)