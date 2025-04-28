from pages.base_page import BasePage


def test_create_project_with_ui(authorized_user: BasePage):
    authorized_user.header.go_to_projects_page()
    authorized_user.page.pause()