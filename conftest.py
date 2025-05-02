import pytest
import requests
from playwright.sync_api import Page, sync_playwright

from api.api_manager import APIManager
from data.build_conf_data import BuildConfData
from data.project_data import ProjectData
from data.rub_build_data import RunBuildData
from data.user_data import UserData
from entities.user import Role, User
from pages.login_page import LoginPage
from resources.user_creds import SuperAdminCreds

@pytest.fixture
def project_data(super_admin):
    created_projects_ids_pool = []

    def _create_project_data():
        project_data = ProjectData.create_project_data()
        created_projects_ids_pool.append(project_data.id)
        return project_data

    yield _create_project_data

    for project_id in created_projects_ids_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)

@pytest.fixture
def build_conf_data():
    def _create_build_conf_data(project_id):
        build_conf_data = BuildConfData.create_build_conf_data(project_id)
        return build_conf_data
    return _create_build_conf_data

@pytest.fixture
def run_build_data():
    def _create_run_build_data(build_id):
        run_build_data = RunBuildData.create_run_build_data(build_id)
        return run_build_data
    return _create_run_build_data

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        new_session = requests.Session()
        user_session = APIManager(new_session)
        user_pool.append(user_session)
        return user_session
    
    yield _create_user_session

    for session in user_pool:
        session.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, None, ['SUPER_ADMIN', 'g'], new_session)
    super_admin.api_manager.auth_api.auth_and_get_csrf_token(super_admin.creds)
    return super_admin

@pytest.fixture
def user_create(user_session, super_admin: User):
    created_users_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, 'g')
        super_admin.api_manager.user_api.create_user(user_data)
        new_session = user_session()
        created_users_pool.append(user_data['username'])
        return User(user_data['username'], user_data['password'], user_data['email'], [Role(role)], new_session)
    
    yield _user_create

    for username in created_users_pool:
        super_admin.api_manager.user_api.delete_user(username)



### UI Fixtures

@pytest.fixture
def browser(scope='session'):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def new_page(browser):
    page = browser.new_page()
    page.set_default_timeout(60000) # x2 of default
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