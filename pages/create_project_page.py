import allure

from pages.base_page import BasePage

class CreationMethodsFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.create_from_url_selector = 'a[href="#createFromUrl"]'
        self.create_manually_selector = 'a[href="#createManually"]'

    def create_from_url(self):
        with allure.step(f'Click selector to create project from URL'):
            self.actions.click_selector(self.create_from_url_selector)

    def create_manually(self):
        with allure.step(f'Click selector to create project manually'):
            self.actions.click_selector(self.create_manually_selector)

    def check_create_manually_button_is_active(self):
        with allure.step('Checks if create manually button is active'):
            self.actions.assert_selector_attribute_has_value(self.create_manually_selector, 'class', 'expanded')

class ProjectCreationFormFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_input_selector = 'input[name="name"]'
        self.project_id_input_selector = 'input#externalId'
        self.project_description_input_selector = 'input#description'
        self.create_project_button_selector = 'input#createProject'

    def fill_manual_creation_fields(self, proj_name, proj_id, proj_desc=''):
        with allure.step(f'Fill manual project creation form with name = "{proj_name}", id = "{proj_id}", desc="{proj_desc}"'):
            self.actions.fill_selector_with_text(self.project_name_input_selector, proj_name)
            self.actions.fill_selector_with_text(self.project_id_input_selector, proj_id)
            self.actions.fill_selector_with_text(self.project_description_input_selector, proj_desc)

    def click_create_proj_button(self):
        with allure.step(f'Click create project button with selector {self.create_project_button_selector}'):
            self.actions.click_selector(self.create_project_button_selector)


class CreateProjectPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu'
        self.creation_methods = CreationMethodsFragment(page)
        self.project_creation_form = ProjectCreationFormFragment(page)
        self.project_creation_confirmation_message_selector = 'div.successMessage'

    def create_project_manually(self, proj_name, proj_id, proj_desc=''):
        with allure.step('Create project manually'):
            self.creation_methods.create_manually()
            self.project_creation_form.fill_manual_creation_fields(proj_name, proj_id, proj_desc)
            self.project_creation_form.click_create_proj_button()