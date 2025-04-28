from actions.page_actions import PageActions


class Header:
    def __init__(self, actions: PageActions):
        self.actions = actions
        self.user_icon_selector = self.actions.page.get_by_role('button', name='admin')
        self.projects_selector = self.actions.page.get_by_role('link', name='Projects')

    def check_login(self):
        self.actions.assert_selector_visible(self.user_icon_selector)

    def go_to_projects_page(self):
        self.actions.click_selector(self.projects_selector)