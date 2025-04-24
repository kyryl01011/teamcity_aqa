import pytest
import requests

from api.api_manager import APIManager


@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope='session')
def api_manager(session):
    return APIManager(session)