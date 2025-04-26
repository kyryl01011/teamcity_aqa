import pytest
import requests

from api.api_manager import APIManager
from data.user_data import UserData
from entities.user import Role, User
from resources.user_creds import SuperAdminCreds


@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def api_manager(session, super_admin_creds):
    api_manager = APIManager(session)
    api_manager.auth_api.auth_api(super_admin_creds)
    return api_manager

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = APIManager(session)
        user_pool.append(user_session)
        return user_session
    
    yield _create_user_session

    for session in user_pool:
        session.close_session()

@pytest.fixture
def super_admin_creds():
    return SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD

@pytest.fixture
def super_admin(user_session, super_admin_creds):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, None, ['SUPER_ADMIN', 'g'], new_session)
    super_admin.api_object.auth_api.auth_api(super_admin_creds)
    return super_admin

@pytest.fixture
def user_create(user_session, super_admin: User):
    created_users_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, 'g')
        super_admin.api_object.user_api.create_user(user_data)
        new_session = user_session()
        created_users_pool.append(user_data['username'])
        return User(user_data['username'], user_data['password'], user_data['email'], [Role(role)], new_session)
    
    yield _user_create

    for username in created_users_pool:
        super_admin.api_object.user_api.delete_user(username)