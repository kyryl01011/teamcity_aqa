import pytest
from playwright.sync_api import sync_playwright, Page

from src.entities.user import User
from src.pages.login_page import LoginPage


@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(slow_mo=3000)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def new_page(browser):
    page = browser.new_page()
    # set length of default timeout for PW actions / give more time to GitHub Actions free machines
    page.set_default_timeout(15000)
    yield page
    page.close()


@pytest.fixture
def authorized_user(new_page: Page, super_admin: User):
    username, password = super_admin.creds
    login_page = LoginPage(new_page)
    login_page.go_to_login_page()
    login_page.fill_login_from(username, password)
    login_page.log_in()
    login_page.header.check_login()
    return login_page
