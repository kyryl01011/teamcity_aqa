from pages.base_page import BasePage


class ProjectsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/favorite/projects'
        self.create_project_button_selector = 'a[title="Create new project"]'

    def go_to_projects_page(self):
        self.actions.go_to_url(self._get_url(self._endpoint))

    def press_create_project_button(self):
        self.actions.click_selector(self.create_project_button_selector)