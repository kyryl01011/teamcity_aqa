import allure

from src.pages.base_page import BasePage
from src.pages.create_project_page import CreationMethodsFragment


class BuildConfCreationFormFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.name_input_selector = 'input#buildTypeName'
        self.id_input_selector = 'input#buildTypeExternalId'
        self.desc_input_selector = 'input#description'
        self.create_build_conf_button_selector = 'input[name="createBuildType"]'

    def fill_manually_creation_form(self, conf_name, conf_id, conf_desc = ''):
        with allure.step(f'Fill build conf creation form '):
            self.actions.fill_selector_with_text(self.name_input_selector, conf_name)
            self.actions.fill_selector_with_text(self.id_input_selector, conf_id)
            self.actions.fill_selector_with_text(self.desc_input_selector, conf_desc)

    def click_create_build_conf_button(self):
        with allure.step(f'Click button: {self.create_build_conf_button_selector} to create manual build conf'):
            self.actions.click_selector(self.create_build_conf_button_selector)

class BuildConfCreationPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.project_id = project_id
        self._endpoint = f'/admin/createObjectMenu.html?projectId={project_id}&showMode=createBuildTypeMenu&cameFromUrl#createManually'
        self.creation_method = CreationMethodsFragment(page)
        self.creation_form = BuildConfCreationFormFragment(page)
        self.successful_creation_selector = 'div.successMessage:has-text("successfully")'

    def go_to_build_conf_creation_page(self):
        with allure.step(f'Go to build configuration creation page: {self._get_url(self._endpoint)}'):
            self.actions.go_to_url(self._get_url(self._endpoint))

    def wait_for_successful_build_conf_creation(self):
        with allure.step(f'Wait for successful build conf creation by waiting selector: {self.successful_creation_selector}'):
            self.actions.wait_selector(self.successful_creation_selector)