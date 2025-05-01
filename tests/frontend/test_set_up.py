

from pages.setup_page import SetupPage


def test_teamcity_server_setup(new_page):
    setup_page = SetupPage(new_page)
    setup_page.set_up()